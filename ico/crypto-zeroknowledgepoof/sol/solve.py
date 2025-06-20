from pwn import *
from Crypto.Util.number import *

class Hash():
    def __init__(self):
        return
    def hash(self, x):
        res = 0
        x = bin(bytes_to_long(x))[2:]
        for i in range(len(x)):
            if x[i] == '1':
                res ^= (1 << (i % 16))
        return res

g = 2
# 512 bit prime
p = 11259801329172779448152544797698355898356717994281608553979880586069417859852688425241082093067347088229999089894449024457276797669841624938789851263644843
q = p - 1

# io = process(["python3","chall.py"])
io = remote("localhost", 33301)

io.recvuntil(b"pubkey = ")
pubkey = int(io.recvline()[:-1].decode())

hasher = Hash()

while True:
    # pick random z and h
    z = getRandomRange(1,q)
    h = getRandomRange(1, (1 << 16))
    print(pow(pubkey, -h, p))
    
    b = (pow(g,z,p) * pow(pubkey, -h, p)) % p 
    print(f"{b = }")
    # print(long_to_bytes(b))
    # print(hasher.hash(long_to_bytes(b)))
    # exit()
    print(f"lhs: {hasher.hash(long_to_bytes(b)) % q}")
    print(f"rhs: {h}")
    if hasher.hash(long_to_bytes(b)) % q == h:
        io.sendlineafter(b"b: ", str(b).encode())
        io.sendlineafter(b"proof: ", str(z).encode())
        io.interactive()
        exit()
