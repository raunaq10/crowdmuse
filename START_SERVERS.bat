@echo off
echo ========================================
echo Starting Attendance System Servers
echo ========================================
echo.

cd /d "C:\Users\singh\OneDrive\Desktop\attendance system"

echo Starting Backend API Server (Port 3001)...
start "Backend API" cmd /k "node server.js"

timeout /t 3 /nobreak >nul

echo Starting Face Recognition Web App (Port 5000)...
cd face_recognition
start "Face Recognition" cmd /k "python web_app.py"

echo.
echo ========================================
echo Servers Starting...
echo ========================================
echo Backend API: http://localhost:3001
echo Web Interface: http://localhost:5000
echo.
echo Press any key to exit this window (servers will keep running)...
pause >nul
