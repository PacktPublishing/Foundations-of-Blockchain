#!/usr/bin/python

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Encryption part
with open("aes.key", "wb") as file_out:
    key = get_random_bytes(16)
    file_out.write(key)
data = "plaintext for AES"
cipher = AES.new(key, AES.MODE_EAX)
cipher_text, tag = cipher.encrypt_and_digest(data.encode())
with open("encrypted.bin", "wb") as file_out:
    [file_out.write(x) for x in (cipher.nonce, tag, cipher_text)]
print("Data is encrypted and stored in a file")


# Decryption part
with open("aes.key", "rb") as file_in:
    key = file_in.read(16)
with open("encrypted.bin", "rb") as file_in:
    nonce, tag, cipher_text = [file_in.read(x) for x in (16, 16, -1)]

# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(cipher_text, tag)
print("Decrypted data is : \"{}\"".format(data.decode()))
