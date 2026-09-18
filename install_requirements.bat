@echo off
chcp 65001 >nul
echo ========================================
echo  Sunone Aimbot - 필수 모듈 설치
echo ========================================
echo.

REM Python 3.12 권장 (supervision, keyboard, screeninfo 등이 3.14 미지원)
py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python 3.12 사용
    py -3.12 -m pip install -r requirements.txt
    goto :done
)

REM 현재 기본 Python으로 시도
echo Python 3.12가 없어 기본 Python으로 설치 시도합니다.
echo (일부 패키지가 설치되지 않으면 Python 3.12 설치를 권장합니다.)
echo.
py -m pip install -r requirements.txt

:done
echo.
echo 설치 완료. 실행: py run.py 또는 run_ai.bat
pause
