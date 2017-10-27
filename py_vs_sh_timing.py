#usr/bin/env python3

import hashlib as hl
import binascii as bs
import subprocess as sub
import time
import itertools

def pypmk(phrase,ssid):
	'''use python libraries'''
	ssid2 = ssid.encode('utf-8')
	phrase2 = phrase.encode('utf-8')
	pmk = hl.pbkdf2_hmac('sha1',phrase2, ssid2, 4096, 32) 
#	print( bs.hexlify(pmk).decode('utf-8') )
	return bs.hexlify(pmk).decode('utf-8')	

def shpmk(phrase,ssid):
	'''use cli tool'''
	p = sub.run("wpa_passphrase "+ssid+" "+phrase, shell="TRUE", stdout=sub.PIPE, universal_newlines="TRUE")
	out1 = p.stdout.split()
#		print(out1[3][4:])
	return out1[3][4:]

def main(func,li, ssid):
	gend =[]
	for i,j in enumerate(li):
		gend.append(func(j,ssid))
		
		#print something to show still alive		
		if (i%100 ==0):
			print(i, func)
	return gend


if __name__=='__main__':

		#initialize
		ssid = 'mywifi'
		charlist = """ABC"""
		inli = [''.join(i) for i in itertools.product(charlist, repeat = 8)]	
		#subset
		li = inli[:1000]

		tic = time.time()
		pyli = main(pypmk, li, ssid)
		
		tic2 = time.time()
		shli = main(shpmk, li, ssid)

		tic3 = time.time()
	
		#calc rates
		total = len(li)
		pytm = tic2-tic
		pyrate = total/pytm
		shtm = tic3-tic2
		shrate = total/shtm
		
		# check for any discrepancies
		for i,(j,k) in enumerate(zip(pyli,shli)):
			if (j != k):
				print(i,j,k)
		
		print("\nHashes:", total )
		print("\nPython:", tic2-tic," Rate: %d/h" % (pyrate*3600)  )
		print("Shell :", tic3-tic2, " Rate: %d/h" % (shrate*3600)  )	
		print("\n\n")	




