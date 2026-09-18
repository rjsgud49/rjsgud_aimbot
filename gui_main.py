# -*- coding: utf-8 -*-
"""
GUI 기반 에임보조 실행기
- 에임보조: config.ini 연동, 단축키/마우스 설정
- 실행: Start로 run.py 실행, Stop으로 종료
"""

import os
import sys
import subprocess
import configparser
import threading
import queue
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Windows: 콘솔 창 숨김
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(PROJECT_DIR, "config.ini")
RUN_SCRIPT = os.path.join(PROJECT_DIR, "run.py")
GUI_LOCK_FILE = os.path.join(tempfile.gettempdir(), "sunone_aimbot_gui.lock")


def _gui_take_lock():
    """GUI 단일 인스턴스: 아주 단순한 락 파일. 이미 있으면 실행 중으로 간주."""
    pid = str(os.getpid())
    try:
        # 새로 만들기 시도. 이미 있으면 FileExistsError.
        with open(GUI_LOCK_FILE, "x") as f:
            f.write(pid)
        return True
    except FileExistsError:
        # 기존 락이 있으면 그냥 실행 중으로 간주
        return False


def _gui_release_lock():
    try:
        if os.path.exists(GUI_LOCK_FILE):
            os.remove(GUI_LOCK_FILE)
    except OSError:
        pass

# Python 3.12 우선
def get_py_cmd():
    for cmd in ("py -3.12", "py", "python3", "python"):
        try:
            if " " in cmd:
                base, rest = cmd.split(None, 1)
                r = subprocess.run([base, rest, "-c", "print(1)"], capture_output=True, cwd=PROJECT_DIR, timeout=5)
            else:
                r = subprocess.run([cmd, "-c", "print(1)"], capture_output=True, cwd=PROJECT_DIR, timeout=5)
            if r.returncode == 0:
                return cmd.split() if " " in cmd else [cmd]
        except Exception:
            continue
    return ["python"]


class ConfigEditor:
    def __init__(self, path=CONFIG_PATH):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.optionxform = str

    def load(self):
        self.config.read(self.path, encoding="utf-8")

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            self.config.write(f)

    def get(self, section, key, fallback=None):
        try:
            if not self.config.has_section(section):
                return fallback
            return self.config.get(section, key, fallback=fallback)
        except Exception:
            return fallback

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sunone Aimbot — 에임보조 GUI")
        self.root.minsize(420, 380)
        self.root.geometry("500x450")
        self.editor = ConfigEditor()
        self.editor.load()
        self.process = None
        self.py_cmd = get_py_cmd()
        self.log_queue = queue.Queue()
        self._log_poll_id = None

        self._build_ui()

    def _build_ui(self):
        nb = ttk.Notebook(self.root)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # ---- 탭: 단축키 ----
        fr_hotkeys = ttk.Frame(nb, padding=8)
        nb.add(fr_hotkeys, text="단축키")
        ttk.Label(fr_hotkeys, text="조준(에임보조) 키:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.var_targeting = tk.StringVar(value=self.editor.get("Hotkeys", "hotkey_targeting", "RightMouseButton"))
        self.cb_targeting = ttk.Combobox(fr_hotkeys, textvariable=self.var_targeting, width=22)
        self.cb_targeting.grid(row=0, column=1, padx=4, pady=2)
        ttk.Label(fr_hotkeys, text="종료 키:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.var_exit = tk.StringVar(value=self.editor.get("Hotkeys", "hotkey_exit", "F2"))
        ttk.Combobox(fr_hotkeys, textvariable=self.var_exit, width=22).grid(row=1, column=1, padx=4, pady=2)
        ttk.Label(fr_hotkeys, text="일시정지 키:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.var_pause = tk.StringVar(value=self.editor.get("Hotkeys", "hotkey_pause", "F3"))
        ttk.Combobox(fr_hotkeys, textvariable=self.var_pause, width=22).grid(row=2, column=1, padx=4, pady=2)
        ttk.Label(fr_hotkeys, text="설정 리로드 키:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.var_reload = tk.StringVar(value=self.editor.get("Hotkeys", "hotkey_reload_config", "F4"))
        ttk.Combobox(fr_hotkeys, textvariable=self.var_reload, width=22).grid(row=3, column=1, padx=4, pady=2)
        self._fill_key_combo(fr_hotkeys)

        # ---- 탭: 실행 ----
        fr_run = ttk.Frame(nb, padding=8)
        nb.add(fr_run, text="실행")
        self.btn_start = ttk.Button(fr_run, text="에임봇 시작 (run.py)", command=self._start)
        self.btn_start.grid(row=0, column=0, padx=4, pady=4)
        self.btn_stop = ttk.Button(fr_run, text="에임봇 종료", command=self._stop, state=tk.DISABLED)
        self.btn_stop.grid(row=0, column=1, padx=4, pady=4)
        self.lbl_status = ttk.Label(fr_run, text="대기 중")
        self.lbl_status.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=4)
        log_frame = ttk.LabelFrame(fr_run, text="로그")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, pady=4)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        fr_run.columnconfigure(0, weight=1)
        fr_run.rowconfigure(2, weight=1)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=60, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # ---- 하단: 저장 ----
        fr_bottom = ttk.Frame(self.root, padding=8)
        fr_bottom.pack(fill=tk.X)
        ttk.Button(fr_bottom, text="config.ini 저장 후 적용", command=self._save_config).pack(side=tk.LEFT, padx=4)
        ttk.Button(fr_bottom, text="닫기", command=self.root.quit).pack(side=tk.RIGHT, padx=4)

    def _key_list(self):
        try:
            from logic.buttons import Buttons
            return sorted(Buttons.KEY_CODES.keys(), key=lambda x: (x.upper() != x, x.upper()))
        except Exception:
            return ["LeftMouseButton", "RightMouseButton", "F2", "F3", "F4"]

    def _fill_key_combo(self, parent):
        keys = self._key_list()
        for w in parent.winfo_children():
            if isinstance(w, ttk.Combobox):
                w["values"] = keys

    def _save_config(self):
        try:
            self.editor.load()
            self.editor.set("Hotkeys", "hotkey_targeting", self.var_targeting.get().strip())
            self.editor.set("Hotkeys", "hotkey_exit", self.var_exit.get().strip())
            self.editor.set("Hotkeys", "hotkey_pause", self.var_pause.get().strip())
            self.editor.set("Hotkeys", "hotkey_reload_config", self.var_reload.get().strip())
            self.editor.save()
            self._log("config.ini 저장됨. 에임봇 실행 중이면 F4로 리로드.")
            messagebox.showinfo("저장", "config.ini 저장됨.\n에임봇이 켜져 있으면 F4로 설정 리로드.")
        except Exception as e:
            messagebox.showerror("저장 실패", str(e))
            self._log("저장 실패: " + str(e))

    def _log(self, msg):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _reader_thread(self, pipe, q):
        try:
            for line in iter(pipe.readline, b""):
                if line:
                    try:
                        q.put(line.decode("utf-8", errors="replace").rstrip())
                    except Exception:
                        q.put(line.decode("cp949", errors="replace").rstrip())
        except Exception:
            pass
        q.put(None)

    def _poll_log(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                if msg is None:
                    self._on_process_exit()
                    break
                self._log(msg)
        except queue.Empty:
            pass
        if self.process is not None and self.process.poll() is not None:
            self._on_process_exit()
        elif self.process is not None:
            self._log_poll_id = self.root.after(150, self._poll_log)

    def _on_process_exit(self):
        if self.process is None:
            return
        self.process = None
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.lbl_status.config(text="대기 중")
        self._log("에임봇 프로세스 종료됨.")
        if self._log_poll_id:
            try:
                self.root.after_cancel(self._log_poll_id)
            except Exception:
                pass
            self._log_poll_id = None

    def _start(self):
        self._save_config()
        if self.process is not None and self.process.poll() is None:
            self._log("이미 실행 중")
            return
        try:
            cmd = self.py_cmd + [RUN_SCRIPT]
            self.process = subprocess.Popen(
                cmd,
                cwd=PROJECT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=CREATE_NO_WINDOW,
                bufsize=1,
            )
            t = threading.Thread(target=self._reader_thread, args=(self.process.stdout, self.log_queue), daemon=True)
            t.start()
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.lbl_status.config(text="실행 중 (로그 아래 확인)")
            self._log("에임봇 시작됨. 종료: [에임봇 종료] 또는 게임에서 F2. 일시정지: F3")
            self._log_poll_id = self.root.after(150, self._poll_log)
        except Exception as e:
            messagebox.showerror("실행 실패", str(e))
            self._log("실행 실패: " + str(e))

    def _stop(self):
        if self.process is None:
            return
        try:
            self.process.terminate()
            self.process.wait(timeout=5)
        except Exception:
            try:
                self.process.kill()
            except Exception:
                pass
        self.process = None
        if self._log_poll_id:
            try:
                self.root.after_cancel(self._log_poll_id)
            except Exception:
                pass
            self._log_poll_id = None
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.lbl_status.config(text="대기 중")
        self._log("에임봇 종료됨.")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _on_close(self):
        if self.process is not None and self.process.poll() is None:
            if messagebox.askyesno("종료", "에임봇이 실행 중입니다. 함께 종료할까요?"):
                self._stop()
        _gui_release_lock()
        self.root.quit()


if __name__ == "__main__":
    os.chdir(PROJECT_DIR)
    if not _gui_take_lock():
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("이미 실행 중", "GUI가 이미 실행 중입니다.\n중복 실행되지 않습니다.")
            root.destroy()
        except Exception:
            print("GUI is already running.")
        sys.exit(0)
    app = App()
    try:
        app.run()
    finally:
        _gui_release_lock()
