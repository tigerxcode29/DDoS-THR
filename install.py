#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import time

# Banner keren: coba pake pyfiglet kalo ada, fallback kalo nggak
def print_banner():
    try:
        from pyfiglet import Figlet
        f = Figlet(font="slant")
        banner = f.renderText("Auto Installer")
        print("\033[1;32m" + banner + "\033[0m")
    except ImportError:
        print("\033[1;32m=== Auto Installer ===\033[0m")

# Auto-detect terminal dan environment
def detect_terminal():
    terminal_info = {}
    terminal_info['TERM'] = os.getenv('TERM', 'Unknown')
    # Cek platform: Termux, Linux, Windows, atau MacOS
    if shutil.which("pkg"):
        terminal_info['platform'] = "Termux (pkg available)"
    elif sys.platform.startswith("linux"):
        terminal_info['platform'] = "Linux"
    elif sys.platform == "win32":
        terminal_info['platform'] = "Windows"
    elif sys.platform == "darwin":
        terminal_info['platform'] = "MacOS"
    else:
        terminal_info['platform'] = "Unknown"
    # Cek ketersediaan perintah pkg, npm, pip
    terminal_info['pkg'] = "Available" if shutil.which("pkg") else "Not Available"
    terminal_info['npm'] = "Available" if shutil.which("npm") else "Not Available"
    terminal_info['pip'] = "Available" if shutil.which("pip") else "Not Available"
    # Ukuran terminal
    try:
        size = shutil.get_terminal_size()
        terminal_info['size'] = f"{size.columns}x{size.lines}"
    except Exception:
        terminal_info['size'] = "Unknown"
    return terminal_info

# Fungsi untuk eksekusi command dan print status-nya dengan style
def run_command(cmd):
    print("\033[1;33m[+] Executing:\033[0m " + cmd)
    try:
        # Meng-capture output biar bisa di-debug kalo perlu
        result = subprocess.run(cmd, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("\033[1;32m[✓] Command succeeded:\033[0m " + cmd)
        if result.stdout:
            print("\033[1;34m[stdout]:\033[0m\n" + result.stdout)
    except subprocess.CalledProcessError as e:
        print("\033[1;31m[!] Command failed:\033[0m " + cmd)
        if e.stderr:
            print("\033[1;31m[stderr]:\033[0m\n" + e.stderr)
    print("-" * 70)
    time.sleep(1)

def main():
    # Bersihkan layar dulu
    os.system('clear' if os.name != 'nt' else 'cls')
    print_banner()
    
    # Tampilkan informasi terminal yang terdeteksi
    term_info = detect_terminal()
    print("\033[1;36m[~] Detected Terminal Info:\033[0m")
    for key, value in term_info.items():
        print(f" - {key}: {value}")
    print()
    
    # Konfirmasi user untuk lanjut
    input("\033[1;35m[?] Tekan Enter untuk memulai proses instalasi...\033[0m")
    print("\n\033[1;35m[~] Starting installation process...\033[0m\n")
    
    # Daftar command instalasi
    commands = [
        "pkg update -y && pkg upgrade -y",
        "pkg install python python-pip openssl-tool tor -y",
        "npm install chalk figlet gradient-string ora",
        "pip install httpx requests scapy socksio dnslib pysocks colorama tqdm rich faker aiohttp paramiko cryptography beautifulsoup4 lxml pycryptodome cfscrape cloudscraper stem",
        "pip install requests colorama pyfiglet",
        "pip install requests beautifulsoup4 python-whois rich",
        "pkg upgrade && pkg install python"
    ]
    
    # Eksekusi tiap command instalasi dengan pengecekan error
    for cmd in commands:
        run_command(cmd)
    
    print("\033[1;32m[✓] Semua perintah berhasil dijalankan.\033[0m")
    print("\033[1;36m[~] Sistem udah siap buat pentest & cyber security tools!\033[0m")
    
    # Tunggu sejenak sebelum menjalankan file dos.py
    time.sleep(2)
    print("\033[1;35m[~] Menjalankan dos.py...\033[0m\n")
    
    # Jalankan file dos.py secara otomatis
    try:
        subprocess.run("python dos.py", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("\033[1;31m[!] Gagal menjalankan dos.py:\033[0m", e)

if __name__ == "__main__":
    main()
