@echo off
cd /d "C:\Users\lenovo\Desktop\farmer app\farmer-app - Copy"

REM ✅ Activate virtual environment
call .venv\Scripts\activate

REM ✅ Start backend (Flask) silently
start /min cmd /c "python -m backend.app"

REM ✅ Start frontend (HTTP) silently
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=http://127.0.0.1:8080 --new-window --window-size=1200,800

REM ✅ Wait a few seconds for servers to boot up
timeout /t 6 /nobreak >nul

REM ✅ Launch Chrome and wait for it to close
start "" /wait "C:\Program Files\Google\Chrome\Application\chrome.exe" http://127.0.0.1:8080

REM ✅ When Chrome is closed, stop both servers
echo Closing FarmerApp servers...
taskkill /IM python.exe /F >nul 2>&1
exit
@echo off
cd /d "C:\Users\lenovo\Desktop\farmer app\farmer-app - Copy"

REM ✅ Activate virtual environment
call .venv\Scripts\activate

REM ✅ Start backend (Flask) silently
start /min cmd /c "python -m backend.app"

REM ✅ Start frontend (HTTP) silently
start /min cmd /c "cd frontend && python -m http.server 8080"

REM ✅ Wait a few seconds for servers to boot up
timeout /t 6 /nobreak >nul

REM ✅ Launch Chrome and wait for it to close
start "" /wait "C:\Program Files\Google\Chrome\Application\chrome.exe" http://127.0.0.1:8080

REM ✅ When Chrome is closed, stop both servers
echo Closing FarmerApp servers...
taskkill /IM python.exe /F >nul 2>&1
exit
