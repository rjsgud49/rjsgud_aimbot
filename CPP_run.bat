@echo off
REM [C++] Run ai.exe. Not Python.
chcp 65001 >nul
cd /d "%~dp0"
title [C++] Run

set "EXE=%~dp0engine\build\dml\Release\ai.exe"
if not exist "%EXE%" (
  echo.
  echo [C++] ai.exe missing
  echo   1^) CPP_build.bat
  echo   2^) CPP_run.bat
  echo.
  pause
  exit /b 1
)

echo [C++] starting %EXE%
echo [Settings] press Home in-game for Korean overlay
start "" "%EXE%"
exit /b 0
