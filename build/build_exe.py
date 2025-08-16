#!/usr/bin/env python3
"""
House Price Prediction - Single Executable Builder

This script creates a standalone executable that includes both the frontend and backend
servers in a single file. The executable will run both servers and automatically
open the application in the default web browser.

Requirements:
    pip install pyinstaller

Usage:
    python build_exe.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Get project root (one level up from build directory)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        print("✓ PyInstaller installed successfully")

def create_main_app():
    """Create the main application file that combines frontend and backend"""
    
    main_app_content = '''"""
House Price Prediction - Standalone Application

This application combines the FastAPI backend and frontend into a single executable.
It automatically starts both servers and opens the application in the default browser.
"""

import uvicorn
import threading
import webbrowser
import time
import os
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def run_backend():
    """Run the backend API server"""
    try:
        # Import the API app
        sys.path.append(get_resource_path('src'))
        from api import app as api_app
        
        logger.info("Starting backend API server on port 8000...")
        uvicorn.run(api_app, host="127.0.0.1", port=8000, log_level="warning")
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        sys.exit(1)

def run_frontend():
    """Run the frontend server"""
    try:
        # Import the frontend app
        sys.path.append(get_resource_path('frontend'))
        from server import frontend_app
        
        logger.info("Starting frontend server on port 8080...")
        uvicorn.run(frontend_app, host="127.0.0.1", port=8080, log_level="warning")
    except Exception as e:
        logger.error(f"Failed to start frontend server: {e}")
        sys.exit(1)

def open_browser():
    """Open the application in the default web browser"""
    time.sleep(3)  # Wait for servers to start
    try:
        url = "http://127.0.0.1:8080"
        logger.info(f"Opening application in browser: {url}")
        webbrowser.open(url)
    except Exception as e:
        logger.warning(f"Could not open browser automatically: {e}")
        print(f"\\nPlease open your web browser and navigate to: http://127.0.0.1:8080")

def main():
    """Main application entry point"""
    print("=" * 60)
    print("  House Price Prediction - Standalone Application")
    print("=" * 60)
    print("Starting servers...")
    print("Backend API: http://127.0.0.1:8000")
    print("Frontend:    http://127.0.0.1:8080")
    print("=" * 60)
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Start browser opener in a separate thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Run frontend in the main thread
        run_frontend()
        
    except KeyboardInterrupt:
        print("\\nApplication shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    # Write the main application file in the build directory
    with open('house_price_app.py', 'w', encoding='utf-8') as f:
        f.write(main_app_content)
    
    print("✓ Created main application file: house_price_app.py")

def create_spec_file():
    """Create PyInstaller spec file for advanced configuration"""
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Project root directory
import os
project_root = r"{PROJECT_ROOT}"

# Get all Python files and data files
src_files = []
for root, dirs, files in os.walk(os.path.join(project_root, 'src')):
    for file in files:
        if file.endswith('.py'):
            rel_root = os.path.relpath(root, project_root)
            src_files.append((os.path.join(root, file), rel_root))

# Frontend files
frontend_files = []
for root, dirs, files in os.walk(os.path.join(project_root, 'frontend')):
    for file in files:
        rel_root = os.path.relpath(root, project_root)
        frontend_files.append((os.path.join(root, file), rel_root))

# Model files
model_files = []
models_dir = os.path.join(project_root, 'models')
if os.path.exists(models_dir):
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            rel_root = os.path.relpath(root, project_root)
            model_files.append((os.path.join(root, file), rel_root))

# Data files
data_files = []
data_dir = os.path.join(project_root, 'data')
if os.path.exists(data_dir):
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.csv'):
                rel_root = os.path.relpath(root, project_root)
                data_files.append((os.path.join(root, file), rel_root))

# Combine all data files
all_datas = src_files + frontend_files + model_files + data_files

a = Analysis(
    ['house_price_app.py'],
    pathex=[project_root],
    binaries=[],
    datas=all_datas,
    hiddenimports=[
        'uvicorn',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.websockets',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'fastapi',
        'fastapi.staticfiles',
        'fastapi.responses',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'pandas',
        'numpy',
        'sklearn',
        'sklearn.ensemble',
        'sklearn.tree',
        'sklearn.utils',
        'joblib',
        'pydantic',
        'xgboost',
        'matplotlib',
        'seaborn',
        'starlette',
        'starlette.staticfiles',
        'starlette.responses',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib.backends._tkagg',
        'PIL.ImageTk',
        'PIL._imagingtk',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HousePricePrediction',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('house_price_app.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ Created PyInstaller spec file: house_price_app.spec")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\\nBuilding executable...")
    print("This may take several minutes...")
    
    try:
        # Build using the spec file for better control
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'house_price_app.spec'
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✓ Executable built successfully!")
            
            # Check if the executable exists
            exe_path = Path('dist/HousePricePrediction.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"✓ Executable created: {exe_path}")
                print(f"  Size: {size_mb:.1f} MB")
                
                # Create a simple readme for the executable
                readme_content = """# House Price Prediction - Standalone Application

## How to Run

1. Double-click `HousePricePrediction.exe`
2. Wait for the servers to start (may take 10-30 seconds on first run)
3. Your default web browser will automatically open the application
4. If the browser doesn't open automatically, navigate to: http://127.0.0.1:8080

## Features

- Predicts house prices using Random Forest and XGBoost models
- Web-based interface for easy input
- Real-time predictions with confidence metrics
- Feature importance analysis
- Model performance metrics

## System Requirements

- Windows 10 or later
- No additional software installation required
- Internet connection not required (runs locally)

## Troubleshooting

1. **Antivirus Warning**: Some antivirus software may flag the executable. This is a false positive due to PyInstaller packaging.
2. **Slow Startup**: First launch may be slow as files are extracted. Subsequent launches will be faster.
3. **Port Conflicts**: If ports 8000 or 8080 are in use, close other applications using these ports.

## Technical Details

- Backend API: FastAPI on port 8000
- Frontend: FastAPI static files on port 8080
- Models: Random Forest and XGBoost (pre-trained)
- Data: Ames Housing Dataset
"""
                
                with open('dist/README.txt', 'w', encoding='utf-8') as f:
                    f.write(readme_content)
                
                print("✓ Created README.txt in dist/ folder")
                
                return True
            else:
                print("✗ Executable not found in expected location")
                return False
        else:
            print("✗ Build failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Build error: {e}")
        return False

def cleanup_build_files():
    """Clean up temporary build files"""
    print("\\nCleaning up build files...")
    
    files_to_remove = [
        'house_price_app.py',
        'house_price_app.spec',
    ]
    
    dirs_to_remove = [
        'build',
        '__pycache__',
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"  Removed: {file}")
    
    for dir in dirs_to_remove:
        if os.path.exists(dir):
            shutil.rmtree(dir)
            print(f"  Removed: {{dir}}/")

def main():
    """Main build process"""
    print("House Price Prediction - Executable Builder")
    print("=" * 50)
    
    # Change to build directory
    os.chdir(Path(__file__).parent)
    print(f"Working directory: {{os.getcwd()}}")
    
    # Check if we're in the right project structure
    required_dirs = ['src', 'frontend', 'models', 'data']
    missing_dirs = [d for d in required_dirs if not (PROJECT_ROOT / d).exists()]
    
    if missing_dirs:
        print(f"✗ Missing required directories in project root: {{missing_dirs}}")
        print(f"Project root: {{PROJECT_ROOT}}")
        return False
    
    try:
        # Step 1: Install PyInstaller
        install_pyinstaller()
        
        # Step 2: Create main application file
        create_main_app()
        
        # Step 3: Create spec file
        create_spec_file()
        
        # Step 4: Build executable
        success = build_executable()
        
        # Step 5: Cleanup
        cleanup_build_files()
        
        if success:
            print("\\n" + "=" * 50)
            print("✓ BUILD SUCCESSFUL!")
            print("=" * 50)
            print("Your executable is ready in the 'build/dist/' folder:")
            print("  - HousePricePrediction.exe")
            print("  - README.txt")
            print("\\nTo test: Double-click HousePricePrediction.exe")
            print("The application will start both servers and open in your browser.")
            return True
        else:
            print("\\n" + "=" * 50)
            print("✗ BUILD FAILED!")
            print("=" * 50)
            return False
            
    except KeyboardInterrupt:
        print("\\nBuild cancelled by user.")
        cleanup_build_files()
        return False
    except Exception as e:
        print(f"\\nUnexpected error: {{e}}")
        cleanup_build_files()
        return False

if __name__ == "__main__":
    success = main()
    input("\\nPress Enter to exit...")
    sys.exit(0 if success else 1)
