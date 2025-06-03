from pwn import *
from Crypto.Hash import HMAC, SHA256

# context.log_level = 'debug'

hmac_key = (1337).to_bytes(16, byteorder='big')
TAG_LEN = 256 // 8

# p = process(["python3", "chall_annotated.py"])
# p = remote("nco.nusgreyhats.org", 443)
p = remote("0.cloud.chals.io", 10585)

p.sendlineafter(b"card!", b"1")
p.recvuntil(b"X  1234 5678 1234 5678                           X\nX  ")
prevname = p.recv(8).decode()
p.recvuntil(b"balance: $")
prevbal = p.recv(3).decode() # string
p.recvuntil(b"code is: ")
prevcardhex = p.recvline()[:-5].decode()
log.info(prevcardhex)
prevcardbytes = bytes.fromhex(prevcardhex)
prevcardct = prevcardbytes[:-TAG_LEN]
prevcardpt = prevname + '\n' + prevbal 
log.info(f"prevcardct: {prevcardct}, prevcardpt: {prevcardpt}")
keystream = xor(prevcardct, prevcardpt)

forged_pt = b'aaa\n13371337'
forged_ct = xor(keystream, forged_pt)
hmac = HMAC.new(hmac_key, digestmod=SHA256)
forged_tag = hmac.update(forged_ct).hexdigest()
payload = forged_ct.hex() + forged_tag
p.sendlineafter(b"card!", b"2")
p.sendlineafter(b"below:", payload.encode())
p.interactive()
