# Quick Start Guide

## Prerequisites
- Python 3.10–3.13
- Poetry (optional but recommended) or use the provided venv setup.

## Install
Using Poetry:
```powershell
poetry install
```

Or using the included setup:
```powershell
python .\setup.py
.\.venv\Scripts\activate
```

## Run the Product
One-step on Windows:
```powershell
.\start_dashboard.bat
```
API → http://localhost:8000
UI  → http://localhost:3000

## Make a Prediction via API
```powershell
.\.venv\Scripts\python.exe .\examples\api_usage_example.py
```

## Recreate Cleaned Dataset
```powershell
.\.venv\Scripts\python.exe .\scripts\clean_data.py
```

## Tests
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
