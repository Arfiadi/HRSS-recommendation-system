@echo off
SETLOCAL EnableExtensions
cd /d "%~dp0"

echo =====================================================================
echo   OptiRack HRSS - System Launcher
echo =====================================================================
echo.
echo  * Menjalankan API Backend (FastAPI) dan Frontend UI (React/Vite).
echo  * Untuk MEMATIKAN kedua program, silakan tekan [Ctrl + C] 
echo    atau tutup jendela command prompt ini.
echo.
echo =====================================================================
echo.

:: Memeriksa apakah virtual environment (.venv) tersedia
if exist .venv\Scripts\python.exe (
    echo [System] Mengaktifkan virtual environment venv...
    call .venv\Scripts\activate.bat
    python run.py
) else (
    echo [System] Virtual environment venv tidak ditemukan.
    echo [System] Menjalankan menggunakan Python sistem...
    python run.py
)

echo.
echo =====================================================================
echo   OptiRack HRSS telah dihentikan bersih.
echo =====================================================================
echo.
pause
