from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits, choice, randrange
import sys
import time

CARD_TEMPLATE = """
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
X   XXX     XXX                                  X
X  X   X   X   X                                 X
X   XXX     XXX                                  X
X                                                X
X  XXXXXXXXXXXXX                                 X
X  X           X                                 X
X  XX         XX                                 X
X    XXXXXXXXX                                   X
X                                                X
X  1234 5678 1234 5678                           X
X  {name}                                      X
X  balance: ${bal}                                 X
X                                                X
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""

TAG_LEN = 256 // 8

aes_key = get_random_bytes(16)
hmac_key = (1337).to_bytes(16, byteorder='big') 

sample_names = ["John Doe", "Jane Soh", "Bob Fong"]

def printslow(text):
    for letter in text:
        print(letter, end='', flush=True)
        time.sleep(0.05)
    sys.stdout.write("\n")
    sys.stdout.flush()

# prints the card containing the name and number, and returns the card in hex
def genCard():
    printslow("\33[34mGenerating your card...\33[0m")
    name = choice(sample_names)
    bal = randrange(100,999)
    time.sleep(1)
    print(CARD_TEMPLATE.format(name=name,bal=str(bal)))
    card_pt = (name + '\n' + str(bal)).encode()
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_key)
    card_ct = cipher.encrypt(card_pt)
    hmac = HMAC.new(hmac_key, digestmod=SHA256)
    tag = hmac.update(card_ct).hexdigest()
    printslow(f"\33[34mYour card code is: {card_ct.hex() + tag}\33[0m")

# returns true iff the card is valid
# takes in a card as hex
def checkCard(card):
    card = bytes.fromhex(card)
    if len(card) < TAG_LEN:
        return (False, "") 
    ct, tag = card[:-TAG_LEN], card[-TAG_LEN:]
    hmac = HMAC.new(hmac_key, digestmod=SHA256)
    correct_tag = hmac.update(ct).digest()
    if correct_tag != tag:
        return (False, "") 
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_key)
    pt = cipher.decrypt(ct).decode()
    if '\n' not in pt:
        return (False, "") 
    return (True, pt)

def giveflag():
    flag = open("flag.txt", "r").read()
    printslow(flag)

printslow("\33[34mWelcome to CyberCard!\33[0m")

for _ in range(2):
    printslow("\33[32mChoose one of the options below:\33[0m")
    printslow("\33[32m1. Generate test card\33[0m")
    printslow("\33[32m2. Test your card!\33[0m")
    c = int(input())
    if c == 1:
        genCard()
    elif c == 2:
        printslow("\33[35mEnter your card below:\33[0m")
        inputcard = input()
        valid, pt = checkCard(inputcard)
        if not valid:
            printslow("\33[31mYou're nothing but a scammer! How dare you call me a scammer? But you are!\33[0m")
            exit()
        separator_idx = pt.find('\n')
        name, bal = pt[:separator_idx], pt[separator_idx+1:]
        if bal == "13371337":
            print(CARD_TEMPLATE.format(name=name,bal=bal))
            giveflag()
            break
        else:
            print(CARD_TEMPLATE.format(name=name,bal=bal))
    else:
        printslow("\33[31mYou're nothing but a scammer! How dare you call me a scammer? But you are!\33[0m")
        exit()

printslow("\33[36mThanks for using CyberCard! Hope you enjoyed :)\33[0m")