cloudera courses


Hashing is a good tool to start hardening your cloud product 



You don't have to be a Bruce Schnier to

integrity
password hashing
tamper-proofing
password verification

key management

RSA

Threat modeling

Secure By Design, Secure By Default

wiping

encryption (stay tuned)

MD5, SHA512, KDF... 

I'm not an expert cryptography, but...

Talk about benchmark, recommended hashes (when to use what), also how NOT to do password hashing:

http://www.unixwiz.net/techtips/iguide-crypto-hashes.html

better: PBKDF2
best: scrypt (once battle-tested)

Also, recommend using battle-tested algorithms and libraries. Not only are other libs of the same algorithm probably slower, but more likely to be flawed...

Point to my new node library, krypto...

Also - ensure randomebytes is checking quality of entropy...