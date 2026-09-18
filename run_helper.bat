@echo off
py -3.12 -m pip --version 2>nul
if %errorlevel% neq 0 (
    echo pip is not installed. Installing...
    py -3.12 -m ensurepip --default-pip
    if %errorlevel% neq 0 (
        echo Failed to install pip automatically. Please install pip manually.
        exit /b 1
    )
)

py -3.12 -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo Streamlit is not installed. Installing...
    py -3.12 -m pip install streamlit
    if %errorlevel% neq 0 (
        echo Failed to install streamlit. Please check your internet connection and try again.
        exit /b 1
    )
)

py -3.12 -m streamlit run helper.py --server.fileWatcherType none