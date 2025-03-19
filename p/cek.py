#!/usr/bin/env python3

import sys
import os
import requests
from bs4 import BeautifulSoup
import whois
import socket
import ssl
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import track

# Gunakan record=True untuk menangkap output yang di-print
console = Console(record=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        return f"Error: {e}"

def get_website_info(url):
    # Tambahin protokol kalo belum ada
    if not url.startswith("http"):
        url = "http://" + url
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        console.print(f"[red][Error][/red] Gagal ambil data dari website: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title Found"
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc_tag["content"].strip() if meta_desc_tag and meta_desc_tag.get("content") else "No Description Found"

    domain = url.split("://")[-1].split("/")[0]
    ip = get_ip(domain)
    # Ambil cookies sebagai dictionary
    cookies = response.cookies.get_dict()

    info = {
        "url": url,
        "domain": domain,
        "ip": ip,
        "status_code": response.status_code,
        "title": title,
        "meta_description": meta_desc,
        "headers": response.headers,
        "cookies": cookies,
    }
    return info

def get_whois_info(url):
    domain = url.split("://")[-1].split("/")[0]
    try:
        whois_info = whois.whois(domain)
        return whois_info
    except Exception as e:
        console.print(f"[red][Error][/red] Gagal ambil WHOIS info: {e}")
        return None

def scan_ports(ip, ports):
    open_ports = []
    for port in track(ports, description="Scanning ports..."):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            continue
    return open_ports

def get_ssl_cert_info(domain, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        return cert
    except Exception as e:
        console.print(f"[yellow]SSL Certificate info tidak tersedia: {e}[/yellow]")
        return None

def display_info(website_info, whois_info, open_ports, cert_info):
    # Website Info Table
    info_table = Table(title="Website Info", box=box.DOUBLE_EDGE, style="cyan")
    info_table.add_column("Field", style="bold magenta", overflow="fold")
    info_table.add_column("Value", style="green", overflow="fold")
    info_table.add_row("URL", website_info.get("url", "N/A"))
    info_table.add_row("Domain", website_info.get("domain", "N/A"))
    info_table.add_row("IP", str(website_info.get("ip", "N/A")))
    info_table.add_row("Status Code", str(website_info.get("status_code", "N/A")))
    info_table.add_row("Title", website_info.get("title", "N/A"))
    info_table.add_row("Meta Description", website_info.get("meta_description", "N/A"))
    console.print(info_table)

    # Server Info Table (dari headers)
    server_info_table = Table(title="Server Info", box=box.SIMPLE_HEAVY, style="blue")
    server_info_table.add_column("Field", style="bold cyan", overflow="fold")
    server_info_table.add_column("Value", style="white", overflow="fold")
    headers = website_info.get("headers", {})
    server_info_table.add_row("Server", headers.get("Server", "N/A"))
    server_info_table.add_row("Content-Type", headers.get("Content-Type", "N/A"))
    server_info_table.add_row("X-Powered-By", headers.get("X-Powered-By", "N/A"))
    server_info_table.add_row("Connection", headers.get("Connection", "N/A"))
    server_info_table.add_row("Cache-Control", headers.get("Cache-Control", "N/A"))
    console.print(server_info_table)

    # All Response Headers Table
    headers_table = Table(title="Response Headers", box=box.SIMPLE_HEAVY, style="yellow")
    headers_table.add_column("Header", style="bold blue", overflow="fold")
    headers_table.add_column("Value", style="white", overflow="fold")
    for key, value in headers.items():
        headers_table.add_row(str(key), str(value))
    console.print(headers_table)

    # Cookies Info Table
    cookies = website_info.get("cookies", {})
    cookies_table = Table(title="Cookies Info", box=box.SIMPLE_HEAVY, style="magenta")
    cookies_table.add_column("Cookie", style="bold cyan", overflow="fold")
    cookies_table.add_column("Value", style="white", overflow="fold")
    if cookies:
        for cookie, value in cookies.items():
            cookies_table.add_row(str(cookie), str(value))
    else:
        cookies_table.add_row("No cookies found", "")
    console.print(cookies_table)

    # WHOIS Info Table
    if whois_info:
        whois_table = Table(title="WHOIS Info", box=box.HEAVY_EDGE, style="bright_blue")
        whois_table.add_column("Field", style="bold magenta", overflow="fold")
        whois_table.add_column("Value", style="white", overflow="fold")
        try:
            for key, value in whois_info.items():
                whois_table.add_row(str(key), str(value))
        except Exception as e:
            whois_table.add_row("Error", f"Parsing error: {e}")
        console.print(whois_table)
    else:
        console.print("[red]WHOIS info tidak tersedia[/red]")

    # Open Ports Table
    ports_table = Table(title="Open Ports", box=box.SIMPLE, style="red")
    ports_table.add_column("Port", style="bold green", overflow="fold")
    if open_ports:
        for port in open_ports:
            ports_table.add_row(str(port))
    else:
        ports_table.add_row("No open ports found")
    console.print(ports_table)

    # SSL Certificate Info Table (jika tersedia)
    if cert_info:
        cert_table = Table(title="SSL Certificate Info", box=box.ROUNDED, style="magenta")
        cert_table.add_column("Field", style="bold cyan", overflow="fold")
        cert_table.add_column("Value", style="white", overflow="fold")
        subject = cert_info.get("subject", [])
        issued_to = ", ".join("=".join(item) for group in subject for item in group) if subject else "N/A"
        issuer = cert_info.get("issuer", [])
        issued_by = ", ".join("=".join(item) for group in issuer for item in group) if issuer else "N/A"
        valid_from = cert_info.get("notBefore", "N/A")
        valid_to = cert_info.get("notAfter", "N/A")
        cert_table.add_row("Issued To", issued_to)
        cert_table.add_row("Issued By", issued_by)
        cert_table.add_row("Valid From", valid_from)
        cert_table.add_row("Valid To", valid_to)
        console.print(cert_table)
    else:
        console.print("[yellow]SSL Certificate info tidak tersedia[/yellow]")

if __name__ == "__main__":
    while True:
        url_input = input("Masukkan URL yang akan discan: ").strip()
        if not url_input:
            console.print("[red]URL tidak boleh kosong.[/red]")
            continue

        clear_screen()
        console.print(Panel.fit(f"[*] Gathering info for: [bold]{url_input}[/bold]", style="bold green"))

        website_info = get_website_info(url_input)
        if website_info is None:
            continue

        # Daftar port umum buat discan
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 3306, 8080, 8443]
        ip_address = website_info.get("ip", "")
        if isinstance(ip_address, str) and "Error" not in ip_address:
            open_ports = scan_ports(ip_address, common_ports)
        else:
            open_ports = []

        whois_info = get_whois_info(url_input)
        domain = website_info.get("domain")
        cert_info = get_ssl_cert_info(domain) if domain else None

        display_info(website_info, whois_info, open_ports, cert_info)

        # Prompt user untuk menyimpan output atau mengulangi scanning
        choice = input("Simpan hasil output? (y/n/r/u): ").strip().lower()
        if choice == "y":
            # Simpan otomatis dengan nama default (hasil.txt, hasil-2.txt, dst.)
            base_filename = "hasil.txt"
            filename = base_filename
            counter = 1
            while os.path.exists(filename):
                counter += 1
                filename = f"hasil-{counter}.txt"
            output_text = console.export_text()
            with open(filename, "w", encoding="utf-8") as f:
                f.write(output_text)
            console.print(f"[green]Hasil output disimpan ke {filename}[/green]")
            break
        elif choice == "r":
            # Minta lokasi file output dari user
            custom_filename = input("Masukkan lokasi file output (misal: /path/to/output.txt): ").strip()
            if custom_filename:
                output_text = console.export_text()
                try:
                    with open(custom_filename, "w", encoding="utf-8") as f:
                        f.write(output_text)
                    console.print(f"[green]Hasil output disimpan ke {custom_filename}[/green]")
                except Exception as e:
                    console.print(f"[red]Gagal menyimpan ke {custom_filename}: {e}[/red]")
            else:
                console.print("[yellow]Tidak ada lokasi yang diberikan, hasil tidak disimpan.[/yellow]")
            break
        elif choice == "u":
            # Ulangi scanning dengan clear dan URL baru
            clear_screen()
            continue
        else:
            console.print("[yellow]Output tidak disimpan.[/yellow]")
            break