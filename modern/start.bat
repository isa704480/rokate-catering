@echo off
setlocal
chcp 65001 >nul
rem ================================================================
rem  Rokate - Modern Dynamic
rem  Sayt:  http://localhost:3002      Admin: http://localhost:3002/admin
rem  Backend: http://localhost:8002
rem  Birinchi ishga tushishda hammasini o'zi o'rnatadi.
rem ================================================================
set "NAME=Modern Dynamic"
set "BPORT=8002"
set "FPORT=3002"
set "VDIR=%~dp0"
set "VENV=%~dp0..\.venv"
set "PY=%VENV%\Scripts\python.exe"
title Rokate %NAME%

echo.
echo ==== Rokate - %NAME% ====

rem --- 1. Python muhiti: rokate-catering\.venv - uchala variant uchun bitta ---
if not exist "%PY%" (
  echo [1/5] Python muhiti yaratilmoqda...
  python -m venv "%VENV%"
  if errorlevel 1 goto :err
)

echo [2/5] Python paketlari tekshirilmoqda...
"%PY%" -m pip install -q -r "%VDIR%backend\requirements.txt"
if errorlevel 1 goto :err

echo [3/5] Baza tayyorlanmoqda...
cd /d "%VDIR%backend"
"%PY%" manage.py migrate --noinput -v 0
if errorlevel 1 goto :err
"%PY%" manage.py seed_demo
if errorlevel 1 goto :err
set "DJANGO_SUPERUSER_USERNAME=admin"
set "DJANGO_SUPERUSER_PASSWORD=admin12345"
set "DJANGO_SUPERUSER_EMAIL=admin@rokate.local"
"%PY%" manage.py createsuperuser --noinput >nul 2>nul

echo [4/5] Frontend paketlari...
cd /d "%VDIR%frontend"
if not exist ".env.local" copy ".env.example" ".env.local" >nul
if not exist "node_modules" call npm install
if errorlevel 1 goto :err

echo [5/5] Serverlar ishga tushmoqda...
start "%NAME% - backend :%BPORT%" /d "%VDIR%backend" cmd /k ""%PY%" manage.py runserver %BPORT%"
start "%NAME% - frontend :%FPORT%" /d "%VDIR%frontend" cmd /k "npm run dev -- -p %FPORT%"

echo.
echo   Sayt:   http://localhost:%FPORT%
echo   Admin:  http://localhost:%FPORT%/admin    login: admin   parol: admin12345
echo   Backend oynasi :%BPORT% va frontend oynasi :%FPORT% ochiq tursin.
echo.
timeout /t 15 >nul
start "" "http://localhost:%FPORT%"
exit /b 0

:err
echo.
echo XATO! Yuqoridagi xabarni o'qing.
pause
exit /b 1
