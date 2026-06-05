#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Runner Script for HRSS Recommendation System
Menjalankan FastAPI backend dan React frontend sekaligus dalam sekali jalan.
"""

import os
import sys
import subprocess
import threading
import time

# ANSI Colors for beautiful logs
COLOR_BACKEND = "\033[94m[API Backend]\033[0m"
COLOR_FRONTEND = "\033[92m[React Frontend]\033[0m"
COLOR_SYSTEM = "\033[93m[System]\033[0m"
COLOR_RESET = "\033[0m"

# Initialize ANSI colors support on Windows
if sys.platform == "win32":
    os.system("")

def safe_print(msg):
    """Mencetak pesan dengan penanganan encoding Unicode yang aman di Windows."""
    try:
        print(msg)
    except UnicodeEncodeError:
        try:
            encoding = sys.stdout.encoding or 'utf-8'
            clean_msg = msg.encode(encoding, errors='replace').decode(encoding)
            print(clean_msg)
        except Exception:
            # Fallback jika encoding gagal total
            try:
                print(msg.encode('ascii', errors='replace').decode('ascii'))
            except Exception:
                pass

def log_stream(stream, prefix, color_code):
    """Membaca output stream baris demi baris dan mencetaknya dengan prefix."""
    for line in iter(stream.readline, b''):
        decoded = line.decode('utf-8', errors='replace').strip()
        if decoded:
            safe_print(f"{color_code} {prefix} | {decoded}")

def check_dependencies():
    """Memeriksa dan menginstal dependensi backend dan frontend jika diperlukan."""
    safe_print(f"{COLOR_SYSTEM} Memeriksa lingkungan dan dependensi...")
    
    # 1. Tentukan executable Python
    if sys.platform == "win32":
        python_exe = os.path.join(".venv", "Scripts", "python.exe")
        pip_exe = os.path.join(".venv", "Scripts", "pip.exe")
    else:
        python_exe = os.path.join(".venv", "bin", "python")
        pip_exe = os.path.join(".venv", "bin", "pip")
        
    if not os.path.exists(python_exe):
        safe_print(f"{COLOR_SYSTEM} Virtual environment (.venv) tidak ditemukan! Menggunakan Python sistem ({sys.executable}).")
        python_exe = sys.executable
        pip_exe = f"{sys.executable} -m pip"
        
    # 2. Periksa dependensi Python backend
    try:
        subprocess.run(
            [python_exe, "-c", "import fastapi, uvicorn, pandas, sklearn, xgboost, dotenv"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        safe_print(f"{COLOR_SYSTEM} Dependensi Python backend ditemukan.")
    except subprocess.CalledProcessError:
        safe_print(f"{COLOR_SYSTEM} Dependensi backend tidak lengkap. Menginstal melalui pip...")
        try:
            if sys.platform == "win32":
                subprocess.run([pip_exe, "install", "-e", ".[api]"], check=True)
            else:
                subprocess.run([python_exe, "-m", "pip", "install", "-e", ".[api]"], check=True)
            safe_print(f"{COLOR_SYSTEM} Berhasil menginstal dependensi backend.")
        except Exception as e:
            safe_print(f"{COLOR_SYSTEM} Gagal menginstal dependensi backend: {e}")
            sys.exit(1)

    # 3. Periksa frontend node_modules
    frontend_path = "frontend"
    node_modules_path = os.path.join(frontend_path, "node_modules")
    if not os.path.exists(node_modules_path):
        safe_print(f"{COLOR_SYSTEM} Folder node_modules tidak ditemukan di {frontend_path}. Menjalankan 'npm install'...")
        try:
            subprocess.run("npm install", shell=True, cwd=frontend_path, check=True)
            safe_print(f"{COLOR_SYSTEM} Berhasil menginstal dependensi frontend.")
        except Exception as e:
            safe_print(f"{COLOR_SYSTEM} Gagal menginstal dependensi frontend: {e}")
            sys.exit(1)
    else:
        safe_print(f"{COLOR_SYSTEM} Dependensi Node.js frontend ditemukan.")

def terminate_process(proc, name):
    """Menghentikan proses dan semua proses anaknya secara bersih."""
    if proc.poll() is None:
        safe_print(f"{COLOR_SYSTEM} Menghentikan proses {name}...")
        if sys.platform == "win32":
            # taskkill /F /T /PID mematikan seluruh process tree di Windows secara paksa
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()

def main():
    check_dependencies()
    
    if sys.platform == "win32":
        python_exe = os.path.join(".venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join(".venv", "bin", "python")
        
    if not os.path.exists(python_exe):
        python_exe = sys.executable
        
    safe_print(f"\n{COLOR_SYSTEM} Memulai API Backend dan React Frontend...")
    
    # Flag creationflags di Windows untuk memisahkan process group
    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP
        
    # Start Backend
    backend_cmd = [
        python_exe, "-m", "uvicorn", "src.api.main:app",
        "--host", "127.0.0.1", "--port", "8000"
    ]
    
    backend_proc = subprocess.Popen(
        backend_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creation_flags
    )
    
    # Start Frontend
    frontend_proc = subprocess.Popen(
        "npm run dev",
        shell=True,
        cwd="frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creation_flags
    )
    
    # Buat threads untuk membaca logs
    t_backend_out = threading.Thread(target=log_stream, args=(backend_proc.stdout, "API", COLOR_BACKEND), daemon=True)
    t_backend_err = threading.Thread(target=log_stream, args=(backend_proc.stderr, "API", COLOR_BACKEND), daemon=True)
    t_frontend_out = threading.Thread(target=log_stream, args=(frontend_proc.stdout, "UI ", COLOR_FRONTEND), daemon=True)
    t_frontend_err = threading.Thread(target=log_stream, args=(frontend_proc.stderr, "UI ", COLOR_FRONTEND), daemon=True)
    
    t_backend_out.start()
    t_backend_err.start()
    t_frontend_out.start()
    t_frontend_err.start()
    
    safe_print(f"{COLOR_SYSTEM} Aplikasi telah berjalan!")
    safe_print(f"{COLOR_SYSTEM} -> Backend API  : http://127.0.0.1:8000")
    safe_print(f"{COLOR_SYSTEM} -> Frontend UI : http://localhost:5173 (atau port yang tertera pada log UI)")
    safe_print(f"{COLOR_SYSTEM} Tekan Ctrl+C untuk menghentikan kedua program sekaligus.\n")
    
    try:
        while True:
            # Periksa apakah salah satu proses terhenti tidak terduga
            if backend_proc.poll() is not None:
                safe_print(f"{COLOR_SYSTEM} Backend terhenti secara tidak terduga dengan kode {backend_proc.poll()}")
                break
            if frontend_proc.poll() is not None:
                safe_print(f"{COLOR_SYSTEM} Frontend terhenti secara tidak terduga dengan kode {frontend_proc.poll()}")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        safe_print(f"\n{COLOR_SYSTEM} Menerima sinyal keluar (Ctrl+C)...")
    finally:
        terminate_process(backend_proc, "Backend API")
        terminate_process(frontend_proc, "Frontend UI")
        safe_print(f"{COLOR_SYSTEM} Semua proses berhasil dihentikan. Sampai jumpa!")

if __name__ == "__main__":
    main()
