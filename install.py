#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

# Banner keren: coba pake pyfiglet kalo ada, kalo enggak fallback aja
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

    # Cek ketersediaan perintah pkg dan npm
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

# Fungsi untuk eksekusi command dan ngeprint status-nya
def run_command(cmd):
    print("\033[1;33m[+] Executing:\033[0m " + cmd)
    process = subprocess.run(cmd, shell=True)
    if process.returncode != 0:
        print("\033[1;31m[!] Command failed:\033[0m " + cmd)
    else:
        print("\033[1;32m[✓] Command succeeded:\033[0m " + cmd)
    print("-" * 50)

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print_banner()
    
    # Tampilkan info terminal yang terdeteksi
    term_info = detect_terminal()
    print("\033[1;36m[~] Terminal Info Detected:\033[0m")
    for key, value in term_info.items():
        print(f" - {key}: {value}")
    print()

    # Konfirmasi untuk lanjut (opsional, bisa lo disable kalo udah yakin)
    input("\033[1;35m[?] Tekan Enter buat lanjut ke proses instalasi...\033[0m")
    print("\n\033[1;35m[~] Starting installation process...\033[0m\n")

    # Daftar command instalasi yang mau dijalanin
    commands = [
        "pkg update -y && pkg upgrade -y",
        "pkg install python python-pip openssl-tool tor -y",
        "npm install chalk figlet gradient-string ora",
        "pip install httpx requests scapy socksio dnslib pysocks colorama tqdm rich faker aiohttp paramiko cryptography beautifulsoup4 lxml pycryptodome cfscrape cloudscraper stem",
        "pip install requests colorama pyfiglet",
        "pip install requests beautifulsoup4 python-whois rich",
        "pkg upgrade && pkg install python"
    ]
    
    # Eksekusi tiap command
    for cmd in commands:
        run_command(cmd)
    
    print("\033[1;32m[✓] All commands executed.\033[0m")
    print("\033[1;36m[~] Cuy, sistem lo udah siap buat pentest & cyber security tools!\033[0m")

if __name__ == "__main__":
    main()
