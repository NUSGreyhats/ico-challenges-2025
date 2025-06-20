from Crypto.Util.number import getStrongPrime, bytes_to_long
import json

NBITS = 2048
e = 65537
p, q = getStrongPrime(NBITS, e = e), getStrongPrime(NBITS, e = e)
if p < q:
    p, q = q, p  # Ensure p is always greater than or equal to q

n = p * q

s = (pow(p, q, n) + pow(q, p, n)) % n

with open("../flag.txt", "rb") as f:
    flag = f.read().strip()

with open("chall.json", "w") as f:
    json.dump({
        "n": n,
        "e": e,
        "c": pow(bytes_to_long(flag), e, n),
        "s": s
    }, f)