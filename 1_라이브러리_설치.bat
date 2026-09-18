@echo off
chcp 65001 >nul
title Sunone Aimbot - 라이브러리 설치

echo.
echo ============================================
echo   Sunone Aimbot - 라이브러리 설치 (Python 3.12)
echo ============================================
echo.

REM 프로젝트 폴더로 이동 (배치 파일이 있는 폴더)
cd /d "%~dp0"

REM Python 3.12 확인
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python 3.12가 설치되어 있지 않습니다.
    echo.
    echo 1. https://www.python.org/downloads/release/python-31210/
    echo 2. "Windows installer (64-bit)" 다운로드
    echo 3. 설치 시 "Add python.exe to PATH" 체크 후 설치
    echo.
    pause
    exit /b 1
)

echo [1/2] Python 3.12 확인됨.
py -3.12 --version
echo.

echo [2/2] requirements.txt 설치 중... (시간이 걸릴 수 있습니다)
echo.
py -3.12 -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [오류] 라이브러리 설치에 실패했습니다. 인터넷 연결을 확인하세요.
    pause
    exit /b 1
)

echo.
echo ----------------------------------------
echo   기본 라이브러리 설치 완료.
echo ----------------------------------------
echo.
echo RTX 2060 Super 등 NVIDIA GPU를 사용하려면
echo PyTorch(CUDA)를 추가로 설치해야 합니다.
echo.
set /p INSTALL_CUDA="지금 PyTorch(CUDA 12.1) 설치할까요? (Y/N): "
if /i "%INSTALL_CUDA%"=="Y" (
    echo.
    echo PyTorch CUDA 12.1 설치 중...
    py -3.12 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    if %errorlevel% equ 0 (
        echo.
        echo PyTorch(CUDA) 설치 완료.
        echo config.ini 에서 AI_device = 0 으로 설정하면 GPU를 사용합니다.
    ) else (
        echo PyTorch 설치 실패. https://pytorch.org/get-started/locally/ 참고.
    )
) else (
    echo PyTorch(CUDA)는 건너뜁니다. CPU만 사용 시 config.ini 에 AI_device = cpu 로 두세요.
)

echo.
echo ============================================
echo   설치 완료.
echo   실행: run_ai.bat 또는 py -3.12 run.py
echo   GPU 사용 시 config.ini 에서 AI_device = 0 확인
echo ============================================
echo.
pause
