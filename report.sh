#!/bin/bash

decrypted=$(python3 - << 'EOF'
import base64, sys, zlib, os
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES

def get_decryption_password():
    enc_pwd_blob = "otHBEjaSrwSa0RHKpvAi+bBRfAKafQ3y8KPM/jjRopggq9gDl7wg6P2H+bi1w+HI/XA="
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
