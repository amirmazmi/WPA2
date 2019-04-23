# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


#!/usr/bin/env python3

#https://www.binpress.com/tutorial/simple-python-parallelism/121

# This script generates the plaintext passphrase for a specific length
# and generates the hash using the cli tool wpa_passphrase.
# - Attempt to use multiple cores

# improvements
# 1. write permutations out straight to file
# 2. read permutation from file in chunks, hash and append


import subprocess as sub
import itertools
import sys
import multiprocessing as mp
import datetime as dt
#import hmac
import hashlib as hl
import binascii as bs


#------------------------------------------------------------------------------
def calcHash( passPhrase):
	ssid = b"MyHomeWifi"
	pmk = hl.pbkdf2_hmac('sha1', str.encode(passPhrase), ssid, 4096, 32)
	return pmk

#------------------------------------------------------------------------------
# wpa_passphrase cannot handle quotes
# !#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\] ^_`abcdefghijklmnopqrstuvwxyz{|}~
#------------------------------------------------------------------------------

if __name__=='__main__':
	li=[]
	charlist = """a2Pd"""
	chunk = 350 # multiprocess chunk size

	try:
		print('\n\tPARALLEL: Running...')
		print("\t  chunk size: {}\n".format(chunk))
		startTime = dt.datetime.now()

		#permutation
		li = [''.join(i) for i in itertools.product(charlist, repeat = 8)]
		sampli = li[:2000]

		if len(sampli)<=20: print(sampli)   # for debugging

		with mp.Pool() as pool:
			result = pool.map( calcHash, sampli, chunk)

			endTime = dt.datetime.now()
		
		
		print(" Plaintext permutations:", format(len(li), ',d') )
		print(" Hash calculated:", format(len(result), ',d'),"\n" )
		# length output is 64
		# 32 bytes; 8 word

		timeTaken = (endTime - startTime)
		minDuration = timeTaken/dt.timedelta(seconds=60)
		hashpersec = len(sampli)/timeTaken.total_seconds()

		print("\tTotal time taken:",
						"\n\t\t in minutes:", format(minDuration,  '.3f'),
						"\n\t\t in seconds:", format( timeTaken.total_seconds(), '.3f' ))
		print("\tHash per second:", format( hashpersec, '.3f') )

		print('\n\n ### DONE ### \n\n\n')

	except KeyboardInterrupt:
		print('\n User Interrupt \n')







































