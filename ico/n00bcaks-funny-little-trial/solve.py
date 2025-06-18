from Crypto.Util.number import long_to_bytes
import json
from math import sqrt

with open("dist/chall.json", "r") as f:
    data = json.load(f)
    n = data["n"]
    e = data["e"]
    c = data["c"]
    s = data["s"]

# Actually, s = p + q mod n. This is due to fermat's little theorem.
p_plus_q = s % n

d = pow(e, -1, n - p_plus_q + 1)
flag = pow(c, d, n)
print(f"Flag: {long_to_bytes(flag)}")
