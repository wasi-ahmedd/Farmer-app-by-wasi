@echo off
title 🌾 FarmerApp Launcher
cd /d "C:\Users\lenovo\Desktop\farmer app\farmer-app - Copy"

REM ✅ Activate virtual environment
call .venv\Scripts\activate

REM ✅ Start backend (Flask) silently
start /min cmd /c "python -m backend.app"

REM ✅ Start frontend (HTTP) silently
start /min cmd /c "cd frontend && python -m http.server 8080"

REM ==========================================================
echo Waiting for backend (port 5000) to start...
:wait_backend
timeout /t 2 /nobreak >nul
netstat -ano | find ":5000" >nul
if errorlevel 1 goto wait_backend
echo ✅ Backend is live!

echo Waiting for frontend (port 8080) to start...
:wait_frontend
timeout /t 2 /nobreak >nul
netstat -ano | find ":8080" >nul
if errorlevel 1 goto wait_frontend
echo ✅ Frontend is live!
REM ==========================================================

REM ✅ Launch FarmerApp in Chrome App Mode
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=http://127.0.0.1:8080 --new-window --window-size=1200,800

REM ✅ Wait for Chrome to close, then stop servers
echo 🌾 Waiting for you to close FarmerApp...
:checkchrome
timeout /t 4 /nobreak >nul
tasklist /FI "IMAGENAME eq chrome.exe" | find /I "chrome.exe" >nul
if not errorlevel 1 goto checkchrome

echo Closing FarmerApp servers...
taskkill /IM python.exe /F >nul 2>&1
echo ✅ Servers stopped successfully.
exit
