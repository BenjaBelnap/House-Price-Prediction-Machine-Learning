@echo off
echo Starting House Price Prediction Dashboard...
echo.

echo Starting API server on port 8000...
start "API Server" cmd /k "cd /d %~dp0 && python src/api.py"

timeout /t 3 /nobreak >nul

echo Starting frontend server on port 3000...
start "Frontend Server" cmd /k "cd /d %~dp0 && python frontend/server.py"

echo.
echo Servers are starting...
echo API Server: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
