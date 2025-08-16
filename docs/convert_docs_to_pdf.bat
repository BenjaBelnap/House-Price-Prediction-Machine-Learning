@echo off
echo Converting documentation to PDFs...
echo.

cd /d "%~dp0"

:: Activate virtual environment if it exists
if exist "..\..\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "..\..\.venv\Scripts\activate.bat"
)

:: Run the conversion script
python convert_to_pdf.py

echo.
echo Conversion complete! Check the 'pdfs' folder for generated files.
pause
