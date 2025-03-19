#!/usr/bin/env python3
import sys
import random

def generate_random_ip():
    """
    Menghasilkan satu IP address acak.
    Untuk keamanan, octet pertama dan terakhir di-generate dari 1 sampai 254,
    sedangkan octet tengah dari 0 sampai 255.
    """
    return f"{random.randint(1,254)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def main():
    # Pastikan argumen command-line benar
    if len(sys.argv) != 3:
        print("Usage: python bots.py <jumlah_ip> <output_file>")
        sys.exit(1)
    
    try:
        count = int(sys.argv[1])
    except ValueError:
        print("Error: jumlah_ip harus berupa angka bulat.")
        sys.exit(1)
    
    output_file = sys.argv[2]
    
    # Generate IP palsu
    ips = [generate_random_ip() for _ in range(count)]
    
    # Tulis ke file output
    with open(output_file, "w") as f:
        for ip in ips:
            f.write(ip + "\n")
    
    print(f"Berhasil menghasilkan {count} IP palsu dan disimpan di {output_file}")

if __name__ == "__main__":
    main()