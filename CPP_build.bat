@echo off
REM [C++] Build DirectML engine. Not Python.
chcp 65001 >nul
cd /d "%~dp0engine"
title [C++] Build DirectML

echo.
echo ========================================
echo  [C++] Build engine (DirectML)
echo  Not Python / not gui_main.py
echo ========================================
echo  Need: Visual Studio C++, CMake, Windows SDK
echo  Next: CPP_run.bat
echo ========================================
echo.

call build_dml.bat
set ERR=%ERRORLEVEL%

echo.
if %ERR% neq 0 (
  echo [C++ build FAILED] see engine\docs\build.md
  pause
  exit /b %ERR%
)

if exist "build\dml\Release\ai.exe" (
  echo [C++ build OK] engine\build\dml\Release\ai.exe
  echo [Next] run CPP_run.bat from project root
) else (
  echo [!] ai.exe not found
)
echo.
pause
