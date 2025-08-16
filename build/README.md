# Building Standalone Executable

This directory contains tools to build a standalone executable of the House Price Prediction application.

## Quick Start

### Option 1: Using the Batch File (Recommended for Windows)
```cmd
cd build
build_executable.bat
```

### Option 2: Using Python Script Directly
```bash
cd build
python build_exe.py
```

## Directory Structure

```
build/
├── build_exe.py              # Main build script
├── build_executable.bat      # Windows batch file for easy execution
├── requirements-build.txt    # Build-specific dependencies
├── README.md                 # This file
└── dist/                     # Output directory (created after build)
    ├── HousePricePrediction.exe
    └── README.txt
```

## What the Build Creates

The build process creates a **single executable file** that includes:
- ✅ FastAPI backend server
- ✅ Frontend web interface  
- ✅ Trained ML models (Random Forest & XGBoost)
- ✅ All required Python libraries
- ✅ Static files (HTML, CSS, JS)
- ✅ Data files for model defaults

## Requirements

### For Building:
- Python 3.8+ with your project virtual environment
- All project dependencies installed (`pip install -r requirements.txt` from project root)
- PyInstaller (automatically installed by the build script)
- Trained models in the `../models/` directory
- Project structure with `src/`, `frontend/`, `models/`, `data/` directories

### For Running the Executable:
- **No Python installation required**
- **No additional dependencies required**
- Windows 10 or later
- ~200MB disk space

## Build Process

The build script performs these steps:

1. **Validates project structure** (checks for required directories)
2. **Installs PyInstaller** (if not already installed)
3. **Creates a main application** that combines frontend and backend
4. **Generates PyInstaller spec** with all required files and dependencies
5. **Builds the executable** (~100-200MB)
6. **Creates documentation** for end users
7. **Cleans up** temporary build files

## Output

After successful build, you'll find in the `build/dist/` folder:
- `HousePricePrediction.exe` - The standalone application
- `README.txt` - Instructions for end users

## Usage of the Executable

1. **Double-click** `HousePricePrediction.exe`
2. **Wait** for servers to start (10-30 seconds first time)
3. **Browser opens automatically** to the application
4. **Use the web interface** to make predictions

The executable runs two local servers:
- Backend API: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:8080`

## Supported Files vs. Single File

### Current Approach: Single File with Embedded Resources
- ✅ **One file** for easy distribution
- ✅ **All models included** (no external model files needed)
- ✅ **All static files embedded** (HTML, CSS, JS)
- ✅ **All data files embedded** for model defaults
- ✅ **No installation** required for end users

### Advantages:
- Extremely portable - just one .exe file
- No risk of missing files
- Easy to share/submit
- No path/dependency issues

### Considerations:
- Larger file size (~100-200MB)
- Slower first startup (files extracted to temp)
- Antivirus may flag (false positive from PyInstaller)

## Troubleshooting

### Build Issues:

1. **Missing directories error**:
   ```
   Error: src directory not found in project root!
   ```
   - Ensure you're running from the `build/` directory
   - Check that project structure has `src/`, `frontend/`, `models/`, `data/` directories

2. **Import errors during build**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt` (from project root)
   - Activate your virtual environment first

3. **Model files not found**:
   - Run the notebook to train and save models first
   - Ensure `models/` directory contains `.joblib` files

4. **Build script location**:
   - The build script must be run from the `build/` directory
   - Use the batch file or `cd build` before running the Python script

### Runtime Issues:

1. **Antivirus blocking**:
   - Add exception for the executable
   - This is a common false positive with PyInstaller

2. **Slow startup**:
   - First run is slower (extracting files)
   - Subsequent runs are faster

3. **Port conflicts**:
   - Close applications using ports 8000 or 8080
   - Restart the executable

## Build Optimization

To reduce executable size:
- The build script excludes unnecessary packages (tkinter, etc.)
- Uses UPX compression when available
- Includes only essential data files
- Excludes test files and documentation

## File Paths and Project Structure

The build script automatically detects the project root and includes:

```
Project Root/
├── src/                 # Backend source code
├── frontend/            # Frontend files (HTML, CSS, JS)
├── models/              # Trained ML models (.joblib files)
├── data/                # Data files (.csv files)
└── build/               # Build tools (this directory)
    ├── build_exe.py
    ├── build_executable.bat
    └── dist/            # Output executable
```

## Testing the Build

Before distributing:

1. **Test on the build machine**:
   ```cmd
   cd build/dist
   HousePricePrediction.exe
   ```

2. **Test on a clean machine** (without Python/dependencies)

3. **Verify all features work**:
   - Model predictions
   - Feature importance display
   - Both Random Forest and XGBoost models
   - Form validation

## File Size Analysis

Typical executable components:
- Python runtime: ~40MB
- ML libraries (sklearn, xgboost): ~80MB  
- Web framework (FastAPI, uvicorn): ~20MB
- Models and data: ~10MB
- Application code: ~5MB
- **Total**: ~150-200MB

This is reasonable for a complete ML application with web interface.

## Alternative: Folder Distribution

If single-file distribution has issues, you can modify the spec file to create a folder distribution instead:

```python
exe = EXE(
    # ... other parameters ...
    onefile=False,  # Change this to False in the spec file
    # ... rest of parameters ...
)
```

This creates a folder with the executable and supporting files, which:
- Starts faster
- Is less likely to trigger antivirus
- Easier to debug
- Requires distributing the entire folder
