# InSp3cT0r

## Write-Up

After extracting chllange attachment, we get a `.webp` image that shows inspector gadget.

After executing a Binary Walk on the image, here what we get :

```
binwalk inspector.webp  
```

```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
91412         0x16514         TIFF image data, little-endian offset of first image directory: 8
92290         0x16882         ELF, 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)
```

So, we try to extract the two files using this command :

```
binwalk -D='.*' inspector.webp  
```

or

```
binwalk -e inspector.webp  
```

After that, when try to print the content of each file using `cat` , you can see that they contains same caracters, with some readable onces, so we execute `strings` on one of the files

```
strings ./_inspector.webp.extracte/16514
```

Here is the result :

```
<?xpacket begin="
" id="W5M0MpCehiHzreSzNTczkc9d"?> <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.5-c021 79.154911, 2013/10/29-11:47:16        "> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stRef="http://ns.adobe.com/xap/1.0/sType/ResourceRef#" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmpMM:OriginalDocumentID="xmp.did:9A600BB613206811AB08AF548ED22A82" xmpMM:DocumentID="xmp.did:C46F128E886711E39008FBC265EA6613" xmpMM:InstanceID="xmp.iid:C46F128D886711E39008FBC265EA6613" xmp:CreatorTool="Adobe Photoshop CC (Macintosh)"> <xmpMM:DerivedFrom stRef:instanceID="xmp.iid:034c7cc3-9c39-4d38-8370-f48686daf929" stRef:documentID="xmp.did:549B9735CDF111E1A5A8D6070ACE5344"/> </rdf:Description> </rdf:RDF> </x:xmpmeta> <?xpacket end="r"?>
/lib64/ld-linux-x86-64.so.2
6vfp*
__cxa_finalize
__libc_start_main
__stack_chk_fail
libc.so.6
GLIBC_2.2.5
GLIBC_2.4
GLIBC_2.34
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
PTE1
u+UH
DevFest2H
2{In5PeCH
tooor_G4H
dG3T}
:*3$"
GCC: (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0
Scrt1.o
__abi_tag
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
file.c
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_start_main@GLIBC_2.34
_ITM_deregisterTMCloneTable
_edata
_fini
__stack_chk_fail@GLIBC_2.4
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
_end
__bss_start
main
__TMC_END__
_ITM_registerTMCloneTable
__cxa_finalize@GLIBC_2.2.5
_init
.symtab
.strtab
.shstrtab
.interp
.note.gnu.property
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.plt.sec
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.data
.bss
.comment
```

and we can notice the flag :

```
...
DevFest2H
2{In5PeCH
tooor_G4H
dG3T}
...
```

Note: You can execute `strings` directly on the `inspector.webp` file, but it will be hard to find the flag since it is seperated by `\n` and the file is a lil bit heavy


## Flag

DevFest22{In5PeCtooor_G4dG3T}
