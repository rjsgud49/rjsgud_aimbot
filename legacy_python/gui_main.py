# -*- coding: utf-8 -*-
"""
GUI 기반 에임보조 실행기
- 설치: requirements / CUDA PyTorch
- 에임보조: config.ini 연동, 단축키 설정
- 실행: Start로 run.py 실행, Stop으로 종료
"""

import os
import sys
import subprocess
import configparser
import threading
import queue
import tempfile
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Windows: 콘솔 창 숨김
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(PROJECT_DIR, "config.ini")
REQ_PATH = os.path.join(PROJECT_DIR, "requirements.txt")
RUN_SCRIPT = os.path.join(PROJECT_DIR, "run.py")
ICON_ICO = os.path.join(PROJECT_DIR, "icon.ico")
ICON_PNG = os.path.join(PROJECT_DIR, "icon.png")
ICON_JPG = os.path.join(PROJECT_DIR, "icon.JPG")
GUI_LOCK_FILE = os.path.join(tempfile.gettempdir(), "sunone_aimbot_gui.lock")
PYTHON_DOWNLOAD_URL = "https://www.python.org/downloads/release/python-31210/"
CUDA_TORCH_INDEX = "https://download.pytorch.org/whl/cu121"

# 설정 탭: (섹션, 한글제목, [(키, 라벨, 타입, 선택지|None), ...])
# 타입: bool | int | float | str | choice
SETTINGS_SCHEMA = [
    (
        "Detection window",
        "탐지 영역",
        [
            ("detection_window_width", "너비", "int", None),
            ("detection_window_height", "높이", "int", None),
            ("circle_capture", "원형 캡처", "bool", None),
        ],
    ),
    (
        "Capture Methods",
        "화면 캡처",
        [
            ("capture_fps", "캡처 FPS", "int", None),
            ("mss_capture", "MSS 캡처", "bool", None),
            ("Bettercam_capture", "Bettercam 캡처", "bool", None),
            ("bettercam_monitor_id", "Bettercam 모니터 ID", "int", None),
            ("bettercam_gpu_id", "Bettercam GPU ID", "int", None),
            ("Obs_capture", "OBS 캡처", "bool", None),
            ("Obs_camera_id", "OBS 카메라 ID", "str", None),
        ],
    ),
    (
        "Aim",
        "조준",
        [
            ("body_y_offset", "몸 조준 Y 오프셋 (머리쪽↑)", "float", None),
            ("disable_headshot", "머리 조준 끄기", "bool", None),
            ("disable_prediction", "예측 끄기", "bool", None),
            ("prediction_interval", "예측 간격", "float", None),
            ("hideout_targets", "은신처 타겟", "bool", None),
            ("third_person", "3인칭", "bool", None),
        ],
    ),
    (
        "Mouse",
        "마우스",
        [
            ("mouse_dpi", "DPI", "int", None),
            ("mouse_sensitivity", "감도 (낮을수록 빠르게 붙음)", "float", None),
            ("mouse_fov_width", "FOV 가로", "int", None),
            ("mouse_fov_height", "FOV 세로", "int", None),
            ("mouse_min_speed_multiplier", "최소 속도 배율", "float", None),
            ("mouse_max_speed_multiplier", "최대 속도 배율", "float", None),
            ("mouse_lock_target", "타겟 잠금", "bool", None),
            ("mouse_auto_aim", "자동 조준", "bool", None),
            ("mouse_ghub", "G HUB 마우스", "bool", None),
            ("mouse_rzr", "Razer 마우스", "bool", None),
        ],
    ),
    (
        "Shooting",
        "사격",
        [
            ("auto_shoot", "자동 사격", "bool", None),
            ("triggerbot", "트리거봇", "bool", None),
            ("force_click", "강제 클릭", "bool", None),
            ("bScope_multiplier", "스코프 배율", "float", None),
        ],
    ),
    (
        "AI",
        "AI",
        [
            ("AI_model_name", "모델 파일", "choice", "models"),
            ("AI_model_image_size", "이미지 크기", "choice", ["320", "640"]),
            ("AI_conf", "탐지 신뢰도 (0.2~0.35)", "float", None),
            ("AI_device", "실행 장치", "choice", ["cpu", "0", "1"]),
            ("AI_enable_AMD", "AMD 사용", "bool", None),
            ("disable_tracker", "트래커 끄기", "bool", None),
        ],
    ),
    (
        "Arduino",
        "아두이노",
        [
            ("arduino_move", "이동에 사용", "bool", None),
            ("arduino_shoot", "사격에 사용", "bool", None),
            ("arduino_port", "포트", "str", None),
            ("arduino_baudrate", "보드레이트", "int", None),
            ("arduino_16_bit_mouse", "16비트 마우스", "bool", None),
        ],
    ),
    (
        "overlay",
        "오버레이",
        [
            ("show_overlay", "오버레이 표시", "bool", None),
            ("overlay_show_borders", "테두리", "bool", None),
            ("overlay_show_boxes", "박스", "bool", None),
            ("overlay_show_target_line", "조준선", "bool", None),
            ("overlay_show_target_prediction_line", "예측선", "bool", None),
            ("overlay_show_labels", "라벨", "bool", None),
            ("overlay_show_conf", "신뢰도", "bool", None),
        ],
    ),
    (
        "Debug window",
        "디버그 창",
        [
            ("show_window", "디버그 창 표시", "bool", None),
            ("show_detection_speed", "탐지 속도", "bool", None),
            ("show_window_fps", "FPS 표시", "bool", None),
            ("show_boxes", "박스", "bool", None),
            ("show_labels", "라벨", "bool", None),
            ("show_conf", "신뢰도", "bool", None),
            ("show_target_line", "조준선", "bool", None),
            ("show_target_prediction_line", "예측선", "bool", None),
            ("show_bScope_box", "스코프 박스", "bool", None),
            ("show_history_points", "히스토리 점", "bool", None),
            ("debug_window_always_on_top", "항상 위", "bool", None),
            ("debug_window_scale_percent", "창 크기 %", "int", None),
        ],
    ),
]

# (표시이름, import 이름) — GUI 자체는 stdlib만 쓰므로 미설치여도 창은 뜸
CHECK_PACKAGES = [
    ("numpy", "numpy"),
    ("opencv-python", "cv2"),
    ("ultralytics", "ultralytics"),
    ("torch", "torch"),
    ("supervision", "supervision"),
    ("mss", "mss"),
    ("keyboard", "keyboard"),
    ("pywin32", "win32api"),
    ("screeninfo", "screeninfo"),
    ("onnxruntime", "onnxruntime"),
]


def _set_app_user_model_id():
    """작업표시줄이 python.exe 아이콘으로 묶이지 않게 고유 ID 설정."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "Sunone.Aimbot.GUI.1"
        )
    except Exception:
        pass


def _hide_console():
    """더블클릭/bat로 뜬 검은 콘솔 숨김."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE
    except Exception:
        pass


def _win_set_hwnd_icon(hwnd, ico_path):
    """Win32로 창/작업표시줄 아이콘을 .ico로 강제 설정."""
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x0010
    LR_DEFAULTSIZE = 0x0040
    WM_SETICON = 0x0080
    ICON_SMALL = 0
    ICON_BIG = 1
    GCL_HICON = -14
    GCL_HICONSM = -34

    user32.LoadImageW.argtypes = [
        wintypes.HINSTANCE,
        wintypes.LPCWSTR,
        wintypes.UINT,
        ctypes.c_int,
        ctypes.c_int,
        wintypes.UINT,
    ]
    user32.LoadImageW.restype = wintypes.HANDLE

    hicon_big = user32.LoadImageW(None, ico_path, IMAGE_ICON, 256, 256, LR_LOADFROMFILE)
    if not hicon_big:
        hicon_big = user32.LoadImageW(
            None, ico_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE
        )
    hicon_small = user32.LoadImageW(None, ico_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)
    if not hicon_small:
        hicon_small = hicon_big
    if not hicon_big:
        return False

    user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_big)
    user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small or hicon_big)

    # 클래스 아이콘도 교체 (작업표시줄 캐시 회피)
    try:
        if ctypes.sizeof(ctypes.c_void_p) == 8:
            user32.SetClassLongPtrW(hwnd, GCL_HICON, hicon_big)
            user32.SetClassLongPtrW(hwnd, GCL_HICONSM, hicon_small or hicon_big)
        else:
            user32.SetClassLongW(hwnd, GCL_HICON, hicon_big)
            user32.SetClassLongW(hwnd, GCL_HICONSM, hicon_small or hicon_big)
    except Exception:
        pass

    # GC 방지용으로 핸들 보관
    kernel32  # silence lint
    return True


def _apply_window_icon(root):
    """창 제목줄 + 작업표시줄 아이콘을 icon.ico로 설정."""
    ico = os.path.abspath(ICON_ICO)
    png = os.path.abspath(ICON_PNG)

    # tk 기본 경로
    try:
        if os.path.isfile(ico):
            root.iconbitmap(ico)
    except Exception:
        pass
    try:
        if os.path.isfile(png):
            img = tk.PhotoImage(file=png)
            root.iconphoto(True, img)
            root._app_icon = img
    except Exception:
        pass

    if sys.platform != "win32" or not os.path.isfile(ico):
        return

    def _force():
        try:
            root.update_idletasks()
            import ctypes
            user32 = ctypes.windll.user32
            hwnd = int(root.winfo_id())
            # Tk HWND → 프레임/루트 창으로 승격
            parent = user32.GetParent(hwnd)
            if parent:
                hwnd = int(parent)
            top = user32.GetAncestor(hwnd, 2)  # GA_ROOT
            if top:
                hwnd = int(top)
            _win_set_hwnd_icon(hwnd, ico)
        except Exception:
            pass

    root.after_idle(_force)
    root.after(100, _force)
    root.after(500, _force)
    root.after(1500, _force)


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        if sys.platform == "win32":
            r = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=CREATE_NO_WINDOW,
            )
            return str(pid) in (r.stdout or "")
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def _gui_take_lock():
    """GUI 단일 인스턴스. 죽은 프로세스의 락은 자동 제거."""
    pid = str(os.getpid())
    try:
        with open(GUI_LOCK_FILE, "x") as f:
            f.write(pid)
        return True
    except FileExistsError:
        old_pid = None
        try:
            with open(GUI_LOCK_FILE, "r") as f:
                old_pid = int((f.read() or "0").strip() or "0")
        except Exception:
            old_pid = 0
        if old_pid and _pid_alive(old_pid):
            return False
        # 좀비 락 → 지우고 다시 잡기
        try:
            os.remove(GUI_LOCK_FILE)
        except OSError:
            return False
        try:
            with open(GUI_LOCK_FILE, "x") as f:
                f.write(pid)
            return True
        except FileExistsError:
            return False


def _gui_release_lock():
    try:
        if os.path.exists(GUI_LOCK_FILE):
            os.remove(GUI_LOCK_FILE)
    except OSError:
        pass


def get_py_cmd():
    """Python 3.12 우선."""
    for cmd in ("py -3.12", "py", "python3", "python"):
        try:
            if " " in cmd:
                base, rest = cmd.split(None, 1)
                r = subprocess.run(
                    [base, rest, "-c", "print(1)"],
                    capture_output=True,
                    cwd=PROJECT_DIR,
                    timeout=5,
                )
            else:
                r = subprocess.run(
                    [cmd, "-c", "print(1)"],
                    capture_output=True,
                    cwd=PROJECT_DIR,
                    timeout=5,
                )
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
        self.root.minsize(520, 480)
        self.root.geometry("580x580")
        _apply_window_icon(self.root)
        self.editor = ConfigEditor()
        self.editor.load()
        self.process = None
        self.py_cmd = get_py_cmd()
        self.log_queue = queue.Queue()
        self._log_poll_id = None
        self._installing = False
        self._last_missing = None  # None=미확인, []=OK, [...] =미설치
        self._py_ver = None
        self._has_nvidia = False
        self._nvidia_name = ""
        self._torch_cuda = False
        self._cuda_needed = False
        self.settings_vars = {}  # (section, key) -> (var, typ)

        self._build_ui()
        self.root.after(200, self._refresh_env_status)

    def _build_ui(self):
        nb = ttk.Notebook(self.root)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.notebook = nb

        # ---- 탭: 설치 ----
        fr_setup = ttk.Frame(nb, padding=8)
        nb.add(fr_setup, text="설치")
        fr_setup.columnconfigure(0, weight=1)

        self.lbl_py = ttk.Label(fr_setup, text="Python: 확인 중...")
        self.lbl_py.grid(row=0, column=0, sticky=tk.W, pady=(0, 2))
        self.lbl_gpu = ttk.Label(fr_setup, text="GPU/CUDA: 확인 중...", wraplength=480, justify=tk.LEFT)
        self.lbl_gpu.grid(row=1, column=0, sticky=tk.W, pady=(0, 2))
        self.lbl_pkgs = ttk.Label(fr_setup, text="라이브러리: 확인 중...", wraplength=480, justify=tk.LEFT)
        self.lbl_pkgs.grid(row=2, column=0, sticky=tk.W, pady=(0, 2))
        self.lbl_device = ttk.Label(
            fr_setup,
            text="실행장치(AI_device): 확인 중...",
            wraplength=480,
            justify=tk.LEFT,
        )
        self.lbl_device.grid(row=3, column=0, sticky=tk.W, pady=(0, 8))

        btn_row = ttk.Frame(fr_setup)
        btn_row.grid(row=4, column=0, sticky=tk.W, pady=2)
        self.btn_check = ttk.Button(btn_row, text="상태 다시 확인", command=self._on_check_clicked)
        self.btn_check.pack(side=tk.LEFT, padx=(0, 4))
        self.btn_install = ttk.Button(btn_row, text="라이브러리 설치", command=self._install_requirements)
        self.btn_install.pack(side=tk.LEFT, padx=4)
        self.btn_cuda = ttk.Button(btn_row, text="CUDA PyTorch 설치", command=self._install_cuda_torch)
        self.btn_cuda.pack(side=tk.LEFT, padx=4)

        btn_row2 = ttk.Frame(fr_setup)
        btn_row2.grid(row=5, column=0, sticky=tk.W, pady=2)
        self.btn_py_dl = ttk.Button(btn_row2, text="Python 3.12 다운로드", command=self._open_python_download)
        self.btn_py_dl.pack(side=tk.LEFT, padx=(0, 4))

        ttk.Label(
            fr_setup,
            text="버튼은 상태에 따라 자동으로 켜지고 꺼집니다. 실행장치(AI_device)는 GPU면 0, 없으면 cpu로 자동 저장됩니다.",
            wraplength=480,
        ).grid(row=6, column=0, sticky=tk.W, pady=(8, 4))

        setup_log = ttk.LabelFrame(fr_setup, text="설치 로그")
        setup_log.grid(row=7, column=0, sticky=tk.NSEW, pady=4)
        fr_setup.rowconfigure(7, weight=1)
        self.setup_log_text = scrolledtext.ScrolledText(setup_log, height=10, width=60, state=tk.DISABLED)
        self.setup_log_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

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

        # ---- 탭: 설정 ----
        fr_settings = ttk.Frame(nb, padding=4)
        nb.add(fr_settings, text="설정")
        self._build_settings_tab(fr_settings)

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
        fr_run.columnconfigure(0, weight=1)
        fr_run.rowconfigure(2, weight=1)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=60, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # ---- 하단: 저장 ----
        fr_bottom = ttk.Frame(self.root, padding=8)
        fr_bottom.pack(fill=tk.X)
        ttk.Button(fr_bottom, text="config.ini 저장 후 적용", command=lambda: self._save_config(silent=False)).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(fr_bottom, text="설정 다시 불러오기", command=self._load_settings_from_ini).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(fr_bottom, text="닫기", command=self.root.quit).pack(side=tk.RIGHT, padx=4)

    def _model_choices(self):
        models_dir = os.path.join(PROJECT_DIR, "models")
        names = []
        if os.path.isdir(models_dir):
            for name in sorted(os.listdir(models_dir)):
                if name.lower().endswith((".pt", ".onnx", ".engine")):
                    names.append(name)
        cur = self.editor.get("AI", "AI_model_name", "")
        if cur and cur not in names:
            names.insert(0, cur)
        return names or ["sunxds_0.5.6.pt"]

    def _build_settings_tab(self, parent):
        tip = ttk.Label(
            parent,
            text="값을 바꾼 뒤 아래 [config.ini 저장 후 적용]을 누르세요. 실행 중이면 F4로 리로드.",
            wraplength=520,
        )
        tip.pack(anchor=tk.W, padx=4, pady=(0, 4))

        canvas = tk.Canvas(parent, highlightthickness=0)
        scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        win_id = canvas.create_window((0, 0), window=inner, anchor=tk.NW)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(win_id, width=e.width),
        )

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._settings_canvas = canvas
        self._model_combo = None

        self.settings_vars = {}
        for section, title, fields in SETTINGS_SCHEMA:
            box = ttk.LabelFrame(inner, text=title, padding=6)
            box.pack(fill=tk.X, padx=4, pady=4)
            for row, (key, label, typ, choices) in enumerate(fields):
                ttk.Label(box, text=label).grid(row=row, column=0, sticky=tk.W, pady=2, padx=(0, 8))
                raw = self.editor.get(section, key, "")
                if typ == "bool":
                    var = tk.BooleanVar(value=str(raw).strip().lower() in ("1", "true", "yes", "on"))
                    ttk.Checkbutton(box, variable=var).grid(row=row, column=1, sticky=tk.W, pady=2)
                elif typ == "choice":
                    if choices == "models":
                        values = self._model_choices()
                    else:
                        values = list(choices or [])
                    var = tk.StringVar(value=str(raw) if raw not in (None, "") else (values[0] if values else ""))
                    cb = ttk.Combobox(box, textvariable=var, values=values, width=28)
                    cb.grid(row=row, column=1, sticky=tk.EW, pady=2)
                    if section == "AI" and key == "AI_model_name":
                        self._model_combo = cb
                else:
                    var = tk.StringVar(value="" if raw is None else str(raw))
                    ttk.Entry(box, textvariable=var, width=30).grid(row=row, column=1, sticky=tk.EW, pady=2)
                box.columnconfigure(1, weight=1)
                self.settings_vars[(section, key)] = (var, typ)

    def _load_settings_from_ini(self):
        try:
            self.editor.load()
            self.var_targeting.set(self.editor.get("Hotkeys", "hotkey_targeting", "RightMouseButton"))
            self.var_exit.set(self.editor.get("Hotkeys", "hotkey_exit", "F2"))
            self.var_pause.set(self.editor.get("Hotkeys", "hotkey_pause", "F3"))
            self.var_reload.set(self.editor.get("Hotkeys", "hotkey_reload_config", "F4"))
            for (section, key), (var, typ) in self.settings_vars.items():
                raw = self.editor.get(section, key, "")
                if typ == "bool":
                    var.set(str(raw).strip().lower() in ("1", "true", "yes", "on"))
                else:
                    var.set("" if raw is None else str(raw))
            if self._model_combo is not None:
                self._model_combo["values"] = self._model_choices()
            self._update_device_label()
            messagebox.showinfo("불러오기", "config.ini 값을 화면에 불러왔습니다.")
        except Exception as e:
            messagebox.showerror("불러오기 실패", str(e))

    def _collect_settings_to_editor(self):
        """단축키 + 설정 탭 값을 editor에 반영 (저장 전)."""
        self.editor.load()
        self.editor.set("Hotkeys", "hotkey_targeting", self.var_targeting.get().strip())
        self.editor.set("Hotkeys", "hotkey_exit", self.var_exit.get().strip())
        self.editor.set("Hotkeys", "hotkey_pause", self.var_pause.get().strip())
        self.editor.set("Hotkeys", "hotkey_reload_config", self.var_reload.get().strip())

        for (section, key), (var, typ) in self.settings_vars.items():
            if typ == "bool":
                val = "True" if var.get() else "False"
            else:
                val = str(var.get()).strip()
                if typ == "int":
                    try:
                        val = str(int(float(val)))
                    except ValueError:
                        raise ValueError(f"[{section}] {key} 정수여야 합니다: {val}")
                elif typ == "float":
                    try:
                        val = str(float(val))
                    except ValueError:
                        raise ValueError(f"[{section}] {key} 숫자여야 합니다: {val}")
            self.editor.set(section, key, val)

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

    def _setup_log(self, msg):
        self.setup_log_text.config(state=tk.NORMAL)
        self.setup_log_text.insert(tk.END, msg + "\n")
        self.setup_log_text.see(tk.END)
        self.setup_log_text.config(state=tk.DISABLED)

    def _py_version_info(self):
        try:
            r = subprocess.run(
                self.py_cmd + ["-c", "import sys; print(sys.version.split()[0])"],
                capture_output=True,
                text=True,
                cwd=PROJECT_DIR,
                timeout=8,
                creationflags=CREATE_NO_WINDOW,
            )
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip()
        except Exception:
            pass
        return None

    def _detect_nvidia_gpu(self):
        """nvidia-smi로 NVIDIA GPU 유무·이름 확인. (name, True) 또는 ('', False)"""
        try:
            r = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=8,
                creationflags=CREATE_NO_WINDOW,
            )
            if r.returncode == 0 and r.stdout.strip():
                names = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
                if names:
                    return (", ".join(names), True)
        except Exception:
            pass
        # 드라이버 없는 경우 WMI로 NVIDIA 어댑터만 확인
        try:
            r = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_VideoController | "
                    "Where-Object { $_.Name -match 'NVIDIA' }).Name",
                ],
                capture_output=True,
                text=True,
                timeout=12,
                creationflags=CREATE_NO_WINDOW,
            )
            if r.returncode == 0 and r.stdout.strip():
                names = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
                if names:
                    return (", ".join(names) + " (드라이버/nvidia-smi 확인 필요)", True)
        except Exception:
            pass
        return ("", False)

    def _torch_cuda_info(self):
        """torch CUDA 사용 가능 여부·버전·디바이스명. torch 없으면 None."""
        code = (
            "import torch\n"
            "ok = torch.cuda.is_available()\n"
            "ver = getattr(torch.version, 'cuda', None) or '-'\n"
            "name = torch.cuda.get_device_name(0) if ok else '-'\n"
            "print(f\"{int(ok)}|{ver}|{name}\")\n"
        )
        try:
            r = subprocess.run(
                self.py_cmd + ["-c", code],
                capture_output=True,
                text=True,
                cwd=PROJECT_DIR,
                timeout=25,
                creationflags=CREATE_NO_WINDOW,
            )
            if r.returncode != 0:
                return None
            line = (r.stdout or "").strip().splitlines()[-1]
            parts = line.split("|", 2)
            if len(parts) < 3:
                return None
            return {
                "available": parts[0] == "1",
                "cuda_ver": parts[1],
                "device": parts[2],
            }
        except Exception:
            return None

    def _missing_packages(self):
        missing = []
        for display, mod in CHECK_PACKAGES:
            r = subprocess.run(
                self.py_cmd + ["-c", f"import {mod}"],
                capture_output=True,
                cwd=PROJECT_DIR,
                timeout=15,
                creationflags=CREATE_NO_WINDOW,
            )
            if r.returncode != 0:
                missing.append(display)
        return missing

    def _apply_ai_device(self, device, silent=False):
        try:
            self.editor.load()
            self.editor.set("AI", "AI_device", str(device))
            self.editor.save()
            msg = f"config.ini AI_device = {device} 저장됨."
            self._setup_log(msg)
            self._update_device_label(device)
            key = ("AI", "AI_device")
            if key in self.settings_vars:
                self.settings_vars[key][0].set(str(device))
            if not silent:
                messagebox.showinfo("설정", msg)
            return True
        except Exception as e:
            if not silent:
                messagebox.showerror("실패", str(e))
            return False

    def _update_device_label(self, device=None):
        if device is None:
            device = (self.editor.get("AI", "AI_device", "cpu") or "cpu").strip()
        if str(device).lower() == "cpu":
            tip = "CPU로 추론"
        else:
            tip = f"GPU #{device} 로 추론"
        self.lbl_device.config(text=f"실행장치(AI_device): {device}  — {tip} (자동 설정)")

    def _sync_ai_device(self):
        """감지 결과에 맞춰 AI_device 자동 저장."""
        if self._torch_cuda:
            cur = (self.editor.get("AI", "AI_device", "") or "").strip().lower()
            if cur != "0":
                self._apply_ai_device("0", silent=True)
            else:
                self._update_device_label("0")
            return
        if self._has_nvidia and self._cuda_needed:
            self._update_device_label(self.editor.get("AI", "AI_device", "cpu"))
            return
        cur = (self.editor.get("AI", "AI_device", "") or "").strip().lower()
        if cur != "cpu":
            self._apply_ai_device("cpu", silent=True)
        else:
            self._update_device_label("cpu")

    def _update_setup_buttons(self):
        """상태에 따라 설치 탭 버튼 on/off."""
        if self._installing:
            self.btn_check.config(state=tk.DISABLED)
            self.btn_install.config(state=tk.DISABLED)
            self.btn_cuda.config(state=tk.DISABLED)
            self.btn_py_dl.config(state=tk.DISABLED)
            return

        has_py = bool(self._py_ver)
        missing = self._last_missing
        libs_ok = missing is not None and len(missing) == 0

        self.btn_check.config(state=tk.NORMAL)

        # Python 있으면 다운로드 비활성
        if has_py:
            self.btn_py_dl.config(state=tk.DISABLED, text="Python 다운로드 (설치됨)")
        else:
            self.btn_py_dl.config(state=tk.NORMAL, text="Python 3.12 다운로드")

        # 라이브러리 모두 있으면 설치 비활성
        if not has_py:
            self.btn_install.config(state=tk.DISABLED, text="라이브러리 설치")
        elif libs_ok:
            self.btn_install.config(state=tk.DISABLED, text="라이브러리 설치 (완료)")
        elif missing is None:
            self.btn_install.config(state=tk.DISABLED, text="라이브러리 설치")
        else:
            self.btn_install.config(state=tk.NORMAL, text="라이브러리 설치")

        # CUDA: NVIDIA + 미준비일 때만
        if not has_py:
            self.btn_cuda.config(state=tk.DISABLED, text="CUDA PyTorch 설치")
        elif self._cuda_needed:
            self.btn_cuda.config(state=tk.NORMAL, text="CUDA PyTorch 설치 (필요)")
        elif self._torch_cuda:
            self.btn_cuda.config(state=tk.DISABLED, text="CUDA PyTorch 설치 (완료)")
        else:
            self.btn_cuda.config(state=tk.DISABLED, text="CUDA PyTorch 설치 (불필요)")

    def _on_check_clicked(self):
        self._setup_log("상태 확인 중...")
        self._refresh_env_status()

    def _refresh_env_status(self):
        self.py_cmd = get_py_cmd()
        ver = self._py_version_info()
        self._py_ver = ver
        if not ver:
            self.lbl_py.config(text="Python: 없음 — [Python 3.12 다운로드] 필요")
            self.lbl_gpu.config(text="GPU/CUDA: Python이 필요합니다")
            self.lbl_pkgs.config(text="라이브러리: Python이 필요합니다")
            self._update_device_label("?")
            self._last_missing = None
            self._cuda_needed = False
            self._torch_cuda = False
            self._update_setup_buttons()
            return

        ok312 = ver.startswith("3.12")
        tip = "" if ok312 else "  (3.12 권장)"
        self.lbl_py.config(text=f"Python: {ver}  [{' '.join(self.py_cmd)}]{tip}")
        self.lbl_gpu.config(text="GPU/CUDA: 확인 중...")
        self.lbl_pkgs.config(text="라이브러리: 확인 중...")
        self._update_setup_buttons()

        def work():
            try:
                gpu_name, has_nvidia = self._detect_nvidia_gpu()
                missing = self._missing_packages()
                torch_info = None
                if "torch" not in missing:
                    torch_info = self._torch_cuda_info()
                torch_cuda = bool(torch_info and torch_info["available"])
                cuda_needed = has_nvidia and not torch_cuda
            except Exception as e:
                self.root.after(
                    0,
                    lambda: (
                        self.lbl_gpu.config(text=f"GPU/CUDA: 확인 실패 ({e})"),
                        self.lbl_pkgs.config(text="라이브러리: 확인 실패"),
                        self._update_setup_buttons(),
                    ),
                )
                return

            def apply():
                self._has_nvidia = has_nvidia
                self._nvidia_name = gpu_name
                self._torch_cuda = torch_cuda
                self._cuda_needed = cuda_needed
                self._last_missing = missing

                if has_nvidia and torch_cuda:
                    gpu_txt = (
                        f"GPU/CUDA: 준비됨 · {torch_info['device']} "
                        f"(torch CUDA {torch_info['cuda_ver']})"
                    )
                elif has_nvidia and torch_info is None:
                    gpu_txt = f"GPU/CUDA: NVIDIA 감지 · {gpu_name} · PyTorch 미설치 → CUDA 설치 필요"
                elif has_nvidia and not torch_cuda:
                    gpu_txt = (
                        f"GPU/CUDA: NVIDIA 감지 · {gpu_name} · "
                        f"torch는 CPU용 → CUDA PyTorch 설치 필요"
                    )
                else:
                    gpu_txt = "GPU/CUDA: NVIDIA 없음 · CPU 모드로 사용"

                self.lbl_gpu.config(text=gpu_txt)

                if missing:
                    self.lbl_pkgs.config(
                        text="라이브러리: 미설치 " + ", ".join(missing)
                    )
                else:
                    self.lbl_pkgs.config(text="라이브러리: 모두 설치됨")

                self._sync_ai_device()
                self._update_setup_buttons()

            self.root.after(0, apply)

        threading.Thread(target=work, daemon=True).start()

    def _set_install_busy(self, busy):
        self._installing = busy
        self._update_setup_buttons()

    def _run_pip(self, args, title, on_success=None):
        if self._installing:
            messagebox.showinfo("설치 중", "이미 설치 작업이 진행 중입니다.")
            return
        if not self._py_version_info():
            messagebox.showerror(
                "Python 없음",
                "Python이 없습니다.\n[Python 3.12 다운로드]로 설치한 뒤\n"
                '"Add python.exe to PATH"를 체크하세요.',
            )
            self._refresh_env_status()
            return

        self.notebook.select(0)
        self._set_install_busy(True)
        self._setup_log(f"--- {title} ---")
        self._setup_log(" ".join(self.py_cmd + ["-m", "pip"] + args))

        def work():
            try:
                proc = subprocess.Popen(
                    self.py_cmd + ["-m", "pip"] + args,
                    cwd=PROJECT_DIR,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    creationflags=CREATE_NO_WINDOW,
                    bufsize=1,
                )
                for line in iter(proc.stdout.readline, b""):
                    if not line:
                        break
                    text = line.decode("utf-8", errors="replace").rstrip()
                    if not text:
                        text = line.decode("cp949", errors="replace").rstrip()
                    self.root.after(0, lambda t=text: self._setup_log(t))
                code = proc.wait()
            except Exception as e:
                self.root.after(0, lambda: self._setup_log(f"오류: {e}"))
                code = 1

            def done():
                self._set_install_busy(False)
                if code == 0:
                    self._setup_log(f"{title} 완료.")
                    if on_success:
                        on_success()
                    else:
                        messagebox.showinfo("완료", f"{title} 완료.")
                        self._refresh_env_status()
                else:
                    self._setup_log(f"{title} 실패 (코드 {code}). 인터넷 연결을 확인하세요.")
                    messagebox.showerror("실패", f"{title} 실패.\n설치 로그를 확인하세요.")
                    self._refresh_env_status()

            self.root.after(0, done)

        threading.Thread(target=work, daemon=True).start()

    def _install_requirements(self):
        if not os.path.isfile(REQ_PATH):
            messagebox.showerror("오류", f"requirements.txt 없음:\n{REQ_PATH}")
            return
        if self._last_missing is not None and len(self._last_missing) == 0:
            messagebox.showinfo("완료", "라이브러리가 이미 모두 설치되어 있습니다.")
            self._refresh_env_status()
            return

        def after_libs():
            gpu_name, has_nvidia = self._detect_nvidia_gpu()
            torch_info = self._torch_cuda_info()
            torch_cuda = bool(torch_info and torch_info["available"])
            self._has_nvidia = has_nvidia
            self._nvidia_name = gpu_name
            self._torch_cuda = torch_cuda
            self._cuda_needed = has_nvidia and not torch_cuda

            if self._cuda_needed:
                self._setup_log(
                    f"NVIDIA GPU 감지: {gpu_name or 'unknown'} → CUDA PyTorch 자동 설치 진행"
                )
                messagebox.showinfo(
                    "CUDA 필요",
                    f"NVIDIA GPU가 감지되었습니다.\n{gpu_name or ''}\n\n"
                    "CUDA용 PyTorch를 이어서 설치합니다.",
                )
                self._install_cuda_torch(ask=False)
            else:
                if torch_cuda:
                    self._apply_ai_device("0", silent=True)
                    messagebox.showinfo("완료", "라이브러리 설치 완료.\nCUDA도 이미 사용 가능합니다.")
                else:
                    self._apply_ai_device("cpu", silent=True)
                    messagebox.showinfo(
                        "완료",
                        "라이브러리 설치 완료.\nNVIDIA GPU가 없어 CPU 모드로 설정했습니다.",
                    )
                self._refresh_env_status()

        self._run_pip(["install", "-r", REQ_PATH], "라이브러리 설치", on_success=after_libs)

    def _install_cuda_torch(self, ask=True):
        if ask:
            gpu_name, has_nvidia = self._detect_nvidia_gpu()
            if not has_nvidia:
                messagebox.showinfo(
                    "CUDA 불필요",
                    "NVIDIA GPU가 감지되지 않았습니다.\nCUDA PyTorch는 설치할 필요 없습니다.",
                )
                self._refresh_env_status()
                return
            torch_info = self._torch_cuda_info()
            if torch_info and torch_info["available"]:
                messagebox.showinfo(
                    "이미 준비됨",
                    f"이미 CUDA를 사용할 수 있습니다.\n{torch_info['device']}",
                )
                self._refresh_env_status()
                return
            if not messagebox.askyesno(
                "CUDA PyTorch",
                f"NVIDIA GPU: {gpu_name or '감지됨'}\n\n"
                "CUDA용 PyTorch(CUDA 12.1)를 설치할까요?",
            ):
                self._refresh_env_status()
                return

        def after_cuda():
            info = self._torch_cuda_info()
            if info and info["available"]:
                self._apply_ai_device("0", silent=True)
                messagebox.showinfo(
                    "완료",
                    f"CUDA PyTorch 설치 완료.\n{info['device']}\nAI_device = 0 으로 설정했습니다.",
                )
            else:
                messagebox.showwarning(
                    "확인 필요",
                    "설치는 끝났지만 torch.cuda 가 아직 비활성입니다.\n"
                    "NVIDIA 드라이버를 최신으로 업데이트한 뒤\n[상태 다시 확인]을 눌러보세요.",
                )
            self._refresh_env_status()

        self._run_pip(
            [
                "install",
                "torch",
                "torchvision",
                "torchaudio",
                "--index-url",
                CUDA_TORCH_INDEX,
            ],
            "CUDA PyTorch 설치",
            on_success=after_cuda,
        )

    def _open_python_download(self):
        webbrowser.open(PYTHON_DOWNLOAD_URL)
        self._setup_log("브라우저에서 Python 다운로드 페이지를 열었습니다. 설치 후 [상태 다시 확인]을 누르세요.")
        self.root.after(1500, self._refresh_env_status)

    def _save_config(self, silent=False):
        try:
            self._collect_settings_to_editor()
            self.editor.save()
            self._update_device_label()
            self._log("config.ini 저장됨. 에임봇 실행 중이면 F4로 리로드.")
            if not silent:
                messagebox.showinfo("저장", "config.ini 저장됨.\n에임봇이 켜져 있으면 F4로 설정 리로드.")
            return True
        except Exception as e:
            messagebox.showerror("저장 실패", str(e))
            self._log("저장 실패: " + str(e))
            return False

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
        if not self._save_config(silent=True):
            return
        if self.process is not None and self.process.poll() is None:
            self._log("이미 실행 중")
            return
        missing = self._last_missing
        if missing is None:
            # 빠른 핵심 패키지만 확인 (UI 멈춤 방지)
            r = subprocess.run(
                self.py_cmd + ["-c", "import ultralytics, torch, cv2"],
                capture_output=True,
                cwd=PROJECT_DIR,
                timeout=20,
                creationflags=CREATE_NO_WINDOW,
            )
            if r.returncode != 0:
                missing = ["(미설치 패키지 있음)"]
        if missing:
            self.notebook.select(0)
            messagebox.showwarning(
                "라이브러리 필요",
                "아직 설치되지 않은 패키지가 있습니다"
                + ((":\n" + ", ".join(missing)) if missing != ["(미설치 패키지 있음)"] else "")
                + "\n\n설치 탭에서 [라이브러리 설치]를 먼저 실행하세요.",
            )
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
    _set_app_user_model_id()
    _hide_console()
    if not _gui_take_lock():
        try:
            root = tk.Tk()
            root.withdraw()
            _apply_window_icon(root)
            messagebox.showinfo("이미 실행 중", "GUI가 이미 실행 중입니다.\n중복 실행되지 않습니다.")
            root.destroy()
        except Exception:
            pass
        sys.exit(0)
    app = App()
    try:
        app.run()
    finally:
        _gui_release_lock()
