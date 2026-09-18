@echo off
REM ============================================================
REM  [Python 전용 / 구버전] 라이브러리 설치
REM  C++ 와 무관. 평소에는 쓰지 마세요. → 루트 CPP_빌드.bat
REM ============================================================
chcp 65001 >nul
cd /d "%~dp0"
title [Python 구버전] 설치
echo.
echo [Python 전용] 구버전 설치입니다. C++ 가 아닙니다.
echo 현재 권장: 프로젝트 루트 CPP_빌드.bat / CPP_실행.bat
echo.
py -3.12 -m pip install -r requirements.txt
pause
