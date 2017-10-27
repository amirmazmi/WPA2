#!/usr/bin/env python3

# source: http://stackoverflow.com/questions/12018920/wpa-handshake-with-python-hashing-difficulties


import hmac
import hashlib as hl
import binascii as bs

passPhrase = b"10zZz10ZZzZ"
ssid       = b"Netgear 2/158"

APmac     = bs.unhexlify("001e2ae0bdd0")
Clientmac = bs.unhexlify("cc08e0620bc8")
ANonce    = bs.unhexlify("61c9a3f5cdcdf5fae5fd760836b8008c863aa2317022c7a202434554fb38452b")
SNonce    = bs.unhexlify("60eff10088077f8b03a0e2fc2fc37e1fe1f30f9f7cfbcfb2826f26f3379c4318")

A    = 	b"Pairwise key expansion"
B    = min(APmac,Clientmac)+max(APmac,Clientmac)+min(ANonce,SNonce)+max(ANonce,SNonce)

data = bs.unhexlify("0103005ffe01090020000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")

#desired output
despmk = "01b809f9ab2fb5dc47984f52fb2d112e13d84ccb6b86d4a7193ec5299f851c48"
desptk = "bf49a95f0494f44427162f38696ef8b6"
desmic = "45282522bc6707d6a70a0317a3ed48f0"

def customPRF512(key,A,B):
	blen = 64
	i    = 0
	R    = b''
	while ( i<=((blen*8+159)/160)):
		glob  = A + chr(0).encode('UTF-8') + B + chr(i).encode('UTF-8')
		hmacsha1 = hmac.new(key, glob, hl.sha1)
		i+=1
		R = R+hmacsha1.digest() 
	return R[:blen]


pmk = hl.pbkdf2_hmac('sha1',passPhrase, ssid, 4096, 32) 
ptk = customPRF512(pmk,A,B)
mic = hmac.new(ptk[0:16],data)

print ("\ndesiredpmk:\t", despmk)
print ("pmk:\t\t", bs.hexlify(pmk).decode('UTF-8'),"\n")

print ("\ndesired ptk:\t", desptk)
print ("ptk:\t\t", bs.hexlify(ptk[0:16]).decode('UTF-8'),"\n")




print ("desired mic:\t", desmic)
print ("mic:\t\t",mic.hexdigest(),"\n")





