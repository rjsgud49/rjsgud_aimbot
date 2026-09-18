# 에임봇(run.py) 단일 인스턴스: 한 번에 하나만 실행
import os
import tempfile

AIMBOT_LOCK_NAME = "sunone_aimbot_run.lock"
AIMBOT_LOCK_FILE = os.path.join(tempfile.gettempdir(), AIMBOT_LOCK_NAME)


def take_lock():
    """아주 단순한 락: 파일이 이미 있으면 실행 중으로 간주."""
    pid = str(os.getpid())
    try:
        with open(AIMBOT_LOCK_FILE, "x") as f:
            f.write(pid)
        return True
    except FileExistsError:
        # 이미 실행 중이라고 보고 새 인스턴스는 바로 종료
        return False


def release():
    try:
        if os.path.exists(AIMBOT_LOCK_FILE):
            os.remove(AIMBOT_LOCK_FILE)
    except OSError:
        pass
