from Crypto.Util.number import *

FLAG = 'ICO{fakeflagfortesting}'

g = 2
# 512 bit prime
p = 11259801329172779448152544797698355898356717994281608553979880586069417859852688425241082093067347088229999089894449024457276797669841624938789851263644843
q = p - 1

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

class Prover:
    def __init__(self, privkey):
        self.privkey = privkey 
        print(f"{privkey = }")
        self.pubkey = pow(g,privkey,p)
        print(f"{self.pubkey = }")
    def prove(self):
        a = getRandomRange(1,q)
        b = pow(g,a,p)
        print(f"{b = }")
        hasher = Hash()
        h = hasher.hash(long_to_bytes(b))
        print(f"{h = }")
        proof = (a + h * self.privkey) % q
        print(f"{proof = }")
        lhs = pow(g,proof,p)
        rhs = (b * pow(self.pubkey,h,p)) % p
        print(f"{lhs = }")
        print(f"{rhs = }")

class Verifier:
    def __init__(self, pubkey):
        self.pubkey = pubkey
    def verify(self):
        b = int(input("b: "))
        hasher = Hash()
        h = hasher.hash(long_to_bytes(b))
        proof = int(input("proof: "))
        lhs = pow(g,proof,p)
        rhs = (b * pow(self.pubkey,h,p)) % p 
        if lhs == rhs:
            print(f"Wow! You actually have the private key! Here you go: {FLAG}")
        else:
            print("Better luck next time!")


privkey = getRandomRange(1,p)
pubkey = pow(g,privkey,p)
print(f"{pubkey = }")
verif = Verifier(pubkey)
verif.verify()