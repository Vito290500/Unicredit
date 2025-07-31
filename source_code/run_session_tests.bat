@echo off
REM Script per eseguire i test di sessione in Docker su Windows
REM Uso: run_session_tests.bat

echo 🐳 ESECUZIONE TEST SESSIONE IN DOCKER
echo =====================================

REM Verifica se Docker è in esecuzione
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker non è in esecuzione!
    pause
    exit /b 1
)

REM Trova il container dell'applicazione
for /f "tokens=*" %%i in ('docker ps --format "{{.Names}}" ^| findstr /i "web app django"') do set CONTAINER_NAME=%%i

if "%CONTAINER_NAME%"=="" (
    echo ❌ Container dell'applicazione non trovato!
    echo Containers disponibili:
    docker ps --format "table {{.Names}}\t{{.Image}}"
    pause
    exit /b 1
)

echo 📦 Usando container: %CONTAINER_NAME%

REM Esegui i test nel container
echo 🧪 Esecuzione test Django...
docker exec -it %CONTAINER_NAME% python manage.py test tests.test_session_management -v 2

echo.
echo 🔄 Esecuzione test diretto...
docker exec -it %CONTAINER_NAME% python tests/test_session_management.py

echo.
echo ✅ Test completati!
pause