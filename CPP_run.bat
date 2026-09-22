@echo off
REM [C++] Run ai.exe without leaving a console open.
chcp 65001 >nul
cd /d "%~dp0"

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

REM ai.exe resolves config/models/icon relative to its working directory (Release).
set "RUNDIR=%~dp0engine\build\dml\Release"
if exist "%~dp0icon.png" if not exist "%RUNDIR%\icon.png" (
  copy /Y "%~dp0icon.png" "%RUNDIR%\icon.png" >nul
)

REM Sync root models\*.onnx into Release\models (DML only sees .onnx next to ai.exe).
if not exist "%RUNDIR%\models" mkdir "%RUNDIR%\models" >nul
if exist "%~dp0models\*.onnx" (
  copy /Y "%~dp0models\*.onnx" "%RUNDIR%\models\" >nul
)

REM Detached GUI process (no console). Home = overlay.
start "" /D "%RUNDIR%" "%EXE%"
exit /b 0
