#!/usr/bin/env python

# this is the original python2 code from:
# http://stackoverflow.com/questions/12018920/wpa-handshake-with-python-hashing-difficulties

import hmac,hashlib,binascii
passPhrase="10zZz10ZZzZ"
ssid        = "Netgear 2/158"
A           = "Pairwise key expansion"
APmac       = binascii.a2b_hex("001e2ae0bdd0")
Clientmac   = binascii.a2b_hex("cc08e0620bc8")
ANonce      = binascii.a2b_hex("61c9a3f5cdcdf5fae5fd760836b8008c863aa2317022c7a202434554fb38452b")
SNonce      = binascii.a2b_hex("60eff10088077f8b03a0e2fc2fc37e1fe1f30f9f7cfbcfb2826f26f3379c4318")
B           = min(APmac,Clientmac)+max(APmac,Clientmac)+min(ANonce,SNonce)+max(ANonce,SNonce)
data        = binascii.a2b_hex("0103005ffe01090020000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")


def customPRF512(key,A,B):
	blen = 64
	i    = 0
	R    = ''
	while i<=((blen*8+159)/160):
		hmacsha1 = hmac.new(key,A+chr(0x00)+B+chr(i),hashlib.sha1)
		i+=1
		R = R+hmacsha1.digest()
	return R[:blen]


pmk     = hashlib.pbkdf2_hmac('sha1',passPhrase, ssid, 4096, 32) 
ptk     = customPRF512(pmk,A,B)
mic     = hmac.new(ptk[0:16],data)

print "\ndesiredpmk:\t","01b809f9ab2fb5dc47984f52fb2d112e13d84ccb6b86d4a7193ec5299f851c48"
print "pmk:\t\t", binascii.b2a_hex(pmk),"\n"
print "desired ptk:\t","bf49a95f0494f44427162f38696ef8b6"
print "ptk:\t\t", binascii.b2a_hex(ptk[0:16]),"\n"
print "desired mic:\t","45282522bc6707d6a70a0317a3ed48f0"
print "mic:\t\t", mic.hexdigest(),"\n"




