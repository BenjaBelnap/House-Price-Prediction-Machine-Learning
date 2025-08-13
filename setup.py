import os
import sys
import venv
import subprocess

def create_virtual_environment():
    """Create a new virtual environment"""
    print("Creating virtual environment...")
    venv.create('.venv', with_pip=True)

def get_python_path():
    """Get the correct python path based on OS"""
    if sys.platform == 'win32':
        return os.path.join('.venv', 'Scripts', 'python.exe')
    return os.path.join('.venv', 'bin', 'python')

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    packages = [
        'pandas',
        'numpy',
        'scikit-learn',
        'xgboost',
        'polars',
        'matplotlib',
        'seaborn',
        'jupyter'
    ]
    
    python_path = get_python_path()
    subprocess.check_call([python_path, '-m', 'pip', 'install'] + packages)

def create_directories():
    """Create project directory structure"""
    print("Creating project directories...")
    directories = ['data', 'models', 'notebooks', 'src']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    """Main setup function"""
    print("Starting project setup...")
    
    # Create directories
    create_directories()
    
    # Create virtual environment
    create_virtual_environment()
    
    # Install requirements
    install_requirements()
    
    print("\nSetup complete! To activate the virtual environment:")
    if sys.platform == 'win32':
        print("Run: .venv\\Scripts\\activate")
    else:
        print("Run: source .venv/bin/activate")
    
    print("\nNext steps:")
    print("1. Download the Ames Housing Dataset from Kaggle")
    print("2. Place the dataset in the 'data' directory")
    print("3. Run 'jupyter notebook' to start working with the notebooks")

if __name__ == '__main__':
    main()
