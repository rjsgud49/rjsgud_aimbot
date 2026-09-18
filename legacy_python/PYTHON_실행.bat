@echo off
REM ============================================================
REM  [Python 전용 / 구버전] run.py 실행
REM  C++ 와 무관. 평소에는 쓰지 마세요. → 루트 CPP_실행.bat
REM ============================================================
chcp 65001 >nul
cd /d "%~dp0"
title [Python 구버전] 실행
echo.
echo [Python 전용] 구버전입니다. C++ ai.exe 가 아닙니다.
echo.
py -3.12 run.py
if errorlevel 1 pause
