"""
In AES GCM mode, 
- 12 bytes of nonce first appended with ctr
ENCRYPTION:
- for the i-th block, first encrypt (iv || i) then xor it with plaintext 
DECRYPTION:
- for the i-th block, encrypt (iv || i) then xor it with ciphertext

this challenge is based on the finding that aes-gcm versions before 0.10.3 had a vulnerability in which the buffer gets decrypted even if the tag is invalid: 
https://security.snyk.io/vuln/SNYK-RUST-AESGCM-5916453

- Because of this, an attacker can decrypt using the same nonce that was given initially, resulting in the operation CT ^ Enc(iv || i) being done to every block
- This allows an attacker to find Enc(iv || i) for all i values for an iv of their choice
- Using this info, every ciphertext block of the encrypted flag can be decrypted
"""

from pwn import *
context.log_level = 'debug'

# p = remote("localhost",33004)
p = process("../distrib/aesgoatedmode")
p.recvuntil(b"Encrypted flag (hex): ")
flag_ct_with_tag = bytes.fromhex(p.recvline()[:-1].decode())
p.recvuntil(b"Nonce (hex): ")
iv = bytes.fromhex(p.recvline()[:-1].decode())

CT_LEN = len(flag_ct_with_tag) - 12 # tag is 12 bytes
flag_ct = flag_ct_with_tag[:CT_LEN]

p.sendlineafter(b"Would you like to (e)ncrypt or (d)ecrypt?\n", b"d")
# if this known plaintext doesn't work just change to something else
my_pt = b'11' * len(flag_ct_with_tag)
my_pt_bytes = b'\x11' * len(flag_ct_with_tag)
p.sendlineafter(b"Enter ciphertext (hex): ", b"11" * len(flag_ct_with_tag))
p.sendlineafter(b"Enter nonce (hex): ", iv.hex().encode())

p.recvuntil(b"Decrypted message (hex): ")
keystream = xor(bytes.fromhex(p.recvline()[:-1].decode()), my_pt_bytes) # this is the keystream used to encrypt the flag
p.close()
flag = xor(flag_ct, keystream)
print(flag)