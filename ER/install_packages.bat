@echo off
echo Installing Python packages: bcrypt, tkcalendar, matplotlib, customtkinter...
echo.

:: Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not installed or not in the PATH. Please install Python and ensure pip is available.
    pause
    exit /b
)

:: Install bcrypt
echo Installing bcrypt...
python -m pip install bcrypt
if %errorlevel% neq 0 (
    echo Failed to install bcrypt. Please check your pip configuration or internet connection.
)

:: Install tkcalendar
echo Installing tkcalendar...
python -m pip install tkcalendar
if %errorlevel% neq 0 (
    echo Failed to install tkcalendar. Please check your pip configuration or internet connection.
)

:: Install matplotlib
echo Installing matplotlib...
python -m pip install matplotlib
if %errorlevel% neq 0 (
    echo Failed to install matplotlib. Please check your pip configuration or internet connection.
)

:: Install customtkinter
echo Installing customtkinter...
python -m pip install customtkinter
if %errorlevel% neq 0 (
    echo Failed to install customtkinter. Please check your pip configuration or internet connection.
)

echo.
echo Installation completed. Press any key to exit.
pause
