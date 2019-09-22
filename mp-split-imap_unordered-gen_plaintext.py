#!/usr/bin/env python3
#
# 	This script will generate permutations of possible plaintext passphrases
# 	for specific passphrase length by splitting the phrases into prefix and
#	generate the permutations 
# 		aaABCDE
#
# 	- attemps to use all cores
# 	- each process writes out to its own prefix file - reduces file size and IO bottleneck
#
#-----------------------------------------------------------------------------------------------------------------------------
import os
import itertools
import sys
import multiprocessing as mp
from time import sleep
import queue
import datetime as dt
import functools
import string

#-----------------------------------------------------------------------------------------------------------------------------
cores=mp.cpu_count()-1

#generate plaintext - small subset since too much time to calculate hash
totcharlen = 8 
prefixlen = 2
charlen = totcharlen - prefixlen
prefix_charset = string.ascii_lowercase	[:7]	
prefix = [ ''.join(x) for x in itertools.product( prefix_charset, repeat=2)]
charlist = string.ascii_uppercase[:7]   #"""ABCDEF"""
combitn = (len(charlist)**charlen)*len(prefix)       #formula is length ^characters

#-----------------------------------------------------------------------------------------------------------------------------
pathfile = os.getcwd()

#-----------------------------------------------------------------------------------------------------------------------------
# wpa_passphrase cannot handle quotes
#  !#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
#-----------------------------------------------------------------------------------------------------------------------------

# generator function
def comb_gen( charlen, charlist):
	return itertools.product(charlist,repeat=charlen)

# function to join the combinations
def gen_text( prechar, charlen,charlist):
	try:
		namefile =  prechar + '.txt' 	#+ '-mp-' + str(totcharlen) + '-char-plaintext.txt'
		outfile = os.path.join(pathfile, 'gendata' , namefile)
		with open(outfile,'w') as f:
			ls = []
			count=0
			for j,i in enumerate( comb_gen(charlen, charlist) ):
				ls.append( ''.join( ( prechar,)+ i) )
				if (j%35000==0 and j!=0):
					f.write( '\n'.join( ls ))
					f.write("\n")
					q.put( len(ls))
					ls = []
					#print( os.getpid(), j)

			f.write( '\n'.join( ls ))
			f.write("\n")
			q.put( len(ls))
			ls=[]
			q.put("end")
		f.close()	
		return

	except Exception as e:
		print( os.getpid(), e)

	return 




if __name__=='__main__':

	sys.stdout.write('\n\033[33m PARALLEL: Running... \n\n\033[0m')
	sys.stdout.flush()

	try:
		startTime=dt.datetime.now()
		print("\t Generating ", format(combitn,',d'), "combinations...\n")
		print( "\t  < [{}]  Prefix length:{}  Prefix comb:{}  >".format(prefix_charset, prefixlen, len(prefix)) )
		print( "\t  < [{}]  Permutation length:{}  >".format(charlist, charlen) )
		q=mp.Queue()
		k=0
		procfin=0
		procfin_cache=0
		try:
			with mp.Pool(cores) as pool:
				print("\n", prefix)
				result = pool.imap_unordered( functools.partial(gen_text, charlen=charlen, charlist=charlist), prefix, 1 )
				
				while(1):
					try:
						que=q.get(timeout=0.05)
						if que == "end":
							procfin += 1
							que = []
							if procfin > procfin_cache:
								#print("procfin: {}    procfin_cache: {}    k: {}  len prefix: {}".format( procfin, procfin_cache, k, len(prefix) ))
								procfin_cache=procfin
							if procfin >= len(prefix):
								print("\n\n\t [+] All processes completed.    procfin: {:d}".format(procfin) )
								break
							continue
						else:
							k += que		
		
					except Exception as e:
						pass		

				q.close()	
				pool.close()
				pool.join()
				print("\n\t Generated {:,d} phrases \n\t\twhere calculated combination were {:,d}".format(k, combitn) ) 
				
		except Exception as e:
			print("\n\t### Entered exception ###\n", e)
			pass

		timeTaken = (dt.datetime.now() - startTime)
		minDuration = timeTaken/dt.timedelta(seconds=60)
		print("\n\t Total time taken",
				" \n\t\t minutes: {:.3f}".format(minDuration ),
				" \n\t\t seconds: {:.3f}".format( timeTaken.total_seconds() ),
				"\n\t\t rate   : {:.5f} million phrases per second".format(  k/(timeTaken.total_seconds()*10**6) ))
                
		sys.stdout.write('\n\n\033[33m ### DONE ### \n\n\n\033[0m')

	except KeyboardInterrupt:
		pool.join()
		pool.close()
		sys.stdout.write('\033[33m') #terminal colour
		sys.stdout.write('\n User Interrupt \n')
#		print("Killed at", k, que[-1])
		sys.stdout.write('\033[0m')	#reset color