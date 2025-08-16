@echo off
echo House Price Prediction - Executable Builder
echo ==========================================
echo.

:: Get the directory where this batch file is located (build directory)
set "BUILD_DIR=%~dp0"
:: Get the project root (one level up from build directory)
set "PROJECT_ROOT=%BUILD_DIR%.."

:: Change to project root to check directories
cd /d "%PROJECT_ROOT%"

:: Check if we're in the right directory structure
if not exist "src\" (
    echo Error: src directory not found in project root!
    echo Project root: %PROJECT_ROOT%
    echo Please ensure this script is in the build/ directory of your project.
    pause
    exit /b 1
)

if not exist "models\" (
    echo Error: models directory not found in project root!
    echo Please ensure models are trained and saved in the models/ directory.
    pause
    exit /b 1
)

if not exist "frontend\" (
    echo Error: frontend directory not found in project root!
    echo Please ensure the frontend directory exists.
    pause
    exit /b 1
)

if not exist "data\" (
    echo Error: data directory not found in project root!
    echo Please ensure the data directory with CSV files exists.
    pause
    exit /b 1
)

echo ✓ All required directories found in project root
echo.

:: Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call ".venv\Scripts\activate.bat"
    echo.
)

:: Change back to build directory and run the build script
cd /d "%BUILD_DIR%"
echo Running build script from: %BUILD_DIR%
echo.

python build_exe.py

echo.
echo Build process completed!
echo Check the 'build/dist' folder for your executable.
pause
