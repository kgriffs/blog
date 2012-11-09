OpenSSL 1.1.0-dev xx XXX xxxx
built on: Mon Oct 22 17:13:11 EDT 2012
options:bn(64,64) rc4(8x,int) des(idx,cisc,16,int) aes(partial) idea(int) blowfish(idx) 
compiler: cc -DOPENSSL_THREADS -D_REENTRANT -DDSO_DLFCN -DHAVE_DLFCN_H -arch x86_64 -O3 -DL_ENDIAN -Wall -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5 -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DWHIRLPOOL_ASM -DGHASH_ASM
The 'numbers' are in 1000s of bytes per second processed.
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes
aes-256 cbc      65178.62k    66526.82k    66550.10k   143229.17k   147595.26k

This OPENSSL_ia32cap bitmask should have the following set:

0x200000000000000
For some reason this wasn't set automatically for me when running openssl CLI on my Mac Pro.

aes-256 cbc      65178.62k    66526.82k    66550.10k   143229.17k   147595.26k
Kurt-Griffithss-Mac-Pro:openssl-SNAP-20121022 kurt$ env /usr/local/ssl/bin/openssl speed aes-256-cbc
Doing aes-256 cbc for 3s on 16 size blocks: 12148772 aes-256 cbc's in 3.00s
Doing aes-256 cbc for 3s on 64 size blocks: 3181144 aes-256 cbc's in 2.99s
Doing aes-256 cbc for 3s on 256 size blocks: 797679 aes-256 cbc's in 2.99s
Doing aes-256 cbc for 3s on 1024 size blocks: 197222 aes-256 cbc's in 2.99s
Doing aes-256 cbc for 3s on 8192 size blocks: 25126 aes-256 cbc's in 3.00s
OpenSSL 1.1.0-dev xx XXX xxxx
built on: Mon Oct 22 17:13:11 EDT 2012
options:bn(64,64) rc4(16x,int) des(idx,cisc,16,int) aes(partial) idea(int) blowfish(idx) 
compiler: cc -DOPENSSL_THREADS -D_REENTRANT -DDSO_DLFCN -DHAVE_DLFCN_H -arch x86_64 -O3 -DL_ENDIAN -Wall -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5 -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DWHIRLPOOL_ASM -DGHASH_ASM
The 'numbers' are in 1000s of bytes per second processed.
type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes
aes-256 cbc      64793.45k    68091.38k    68296.26k    67543.59k    68610.73k
