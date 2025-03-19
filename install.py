#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import time
import threading

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
    terminal_info['pkg'] = "Available" if shutil.which("pkg") else "Not Available"
    terminal_info['npm'] = "Available" if shutil.which("npm") else "Not Available"
    terminal_info['pip'] = "Available" if shutil.which("pip") else "Not Available"
    try:
        size = shutil.get_terminal_size()
        terminal_info['size'] = f"{size.columns}x{size.lines}"
    except Exception:
        terminal_info['size'] = "Unknown"
    return terminal_info

# Fungsi animasi spinner sederhana
def spinner(msg, duration=3):
    spinner_chars = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        print(f"\r\033[1;33m{msg} {spinner_chars[idx % len(spinner_chars)]}\033[0m", end='', flush=True)
        time.sleep(0.1)
        idx += 1
    print("\r" + " " * (len(msg)+4), end='\r')

# Fungsi animasi loading bar
def loading_bar(msg, duration=3, length=30):
    print(f"\033[1;34m{msg}\033[0m")
    for i in range(length+1):
        percent = int((i/length)*100)
        bar = "#" * i + "-" * (length-i)
        print(f"\r[{bar}] {percent}%", end='', flush=True)
        time.sleep(duration/length)
    print("\n")

# Fungsi untuk eksekusi command dengan animasi dan logging
def run_command(cmd):
    print("\033[1;33m[+] Executing:\033[0m " + cmd)
    spinner("Loading", duration=2)
    try:
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

# Fungsi untuk proses instalasi modul
def install_modules():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_banner()
    term_info = detect_terminal()
    print("\033[1;36m[~] Detected Terminal Info:\033[0m")
    for key, value in term_info.items():
        print(f" - {key}: {value}")
    print()
    
    input("\033[1;35m[?] Tekan Enter untuk memulai instalasi...\033[0m")
    print("\n\033[1;35m[~] Starting installation process...\033[0m\n")
    
    commands = [
        "pkg update -y && pkg upgrade -y",
        "pkg install python python-pip openssl-tool tor -y",
        "npm install chalk figlet gradient-string ora",
        "pip install httpx requests scapy socksio dnslib pysocks colorama tqdm rich faker aiohttp paramiko cryptography beautifulsoup4 lxml pycryptodome cfscrape cloudscraper stem",
        "pip install requests colorama pyfiglet",
        "pip install requests beautifulsoup4 python-whois rich",
        "pkg upgrade && pkg install python"
    ]
    
    for cmd in commands:
        run_command(cmd)
    
    loading_bar("Finalizing installation...", duration=3)
    print("\033[1;32m[✓] Semua perintah berhasil dijalankan.\033[0m")
    print("\033[1;36m[~] Sistem udah siap buat pentest & cyber security tools!\033[0m")
    time.sleep(2)
    print("\033[1;35m[~] Menjalankan dos.py...\033[0m\n")
    
    # Menjalankan dos.py dengan Popen supaya biar dos.py terus berjalan
    try:
        subprocess.Popen("python dos.py", shell=True)
    except Exception as e:
        print("\033[1;31m[!] Gagal menjalankan dos.py:\033[0m", e)
    
    input("\033[1;35m[?] Tekan Enter untuk kembali ke menu utama...\033[0m")

# Fungsi untuk menjalankan dos.py saja
def run_dos():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_banner()
    loading_bar("Menyiapkan dos.py...", duration=2)
    try:
        subprocess.Popen("python dos.py", shell=True)
    except Exception as e:
        print("\033[1;31m[!] Gagal menjalankan dos.py:\033[0m", e)
    input("\033[1;35m[?] Tekan Enter untuk kembali ke menu utama...\033[0m")

# Menu interaktif
def menu():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        print_banner()
        print("\033[1;36m=== Menu Utama ===\033[0m")
        print("\033[1;33m1.\033[0m Mulai proses instalasi modul")
        print("\033[1;33m2.\033[0m Jalankan dos.py")
        print("\033[1;33m3.\033[0m Keluar")
        choice = input("\033[1;35m[?] Pilih opsi (1/2/3): \033[0m")
        if choice == '1':
            install_modules()
        elif choice == '2':
            run_dos()
        elif choice == '3':
            print("\033[1;32m[✓] Sampai jumpa, bro!\033[0m")
            time.sleep(1)
            break
        else:
            print("\033[1;31m[!] Opsi tidak valid, silakan coba lagi.\033[0m")
            time.sleep(2)

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    menu()

if __name__ == "__main__":
    main()
