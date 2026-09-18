@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Aimbot Install

echo.
echo [1/2] Python 3.12 확인...
py -3.12 --version
if errorlevel 1 (
    echo.
    echo Python 3.12가 없습니다.
    echo https://www.python.org/downloads/release/python-31210/
    echo 설치 시 "Add python.exe to PATH" 체크 후 다시 실행하세요.
    pause
    exit /b 1
)

echo.
echo [2/2] 라이브러리 설치 중...
py -3.12 -m pip install -r requirements.txt
if errorlevel 1 (
    echo 설치 실패. 인터넷 연결을 확인하세요.
    pause
    exit /b 1
)

echo.
echo NVIDIA GPU가 있으면 CUDA용 PyTorch도 설치하세요:
echo   py -3.12 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
echo.
echo 설치 완료. 실행: run_gui.bat
echo.
pause
