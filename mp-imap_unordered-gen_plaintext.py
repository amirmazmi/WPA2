#!/usr/bin/env python3
#
# This script will generate permutations of possible plaintext passphrases
# for specific passphrase length USING QUEUE(SLOW)
#
# - attemps to use all cores - but has significant overhead
# - Write out in small chunks to save RAM space
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
charlen = 7
charlist = string.ascii_uppercase[:7]   #"""ABCDEF"""
prefix_char = string.ascii_lowercase	# here send different first letter to each process
combitn = (len(charlist)**charlen)*len(prefix_char)       #formula is length ^characters

#-----------------------------------------------------------------------------------------------------------------------------
pathfile = os.getcwd()
namefile = 'RUNNING-' + 'mp-' + str(charlen+1) + '-char-plaintext.txt'
outfile = os.path.join(pathfile,namefile)


#-----------------------------------------------------------------------------------------------------------------------------
# wpa_passphrase cannot handle quotes
#  !#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
#-----------------------------------------------------------------------------------------------------------------------------

# generator function
def comb_gen( charlen, charlist):
	return itertools.product(charlist,repeat=charlen)

# function to join the combinations
def gen_text( prechar, charlen,charlist):
	ls = []
	for j,i in enumerate( comb_gen(charlen, charlist) ):
		ls.append( ''.join( ( prechar,)+ i) )
		if (j%75000==0 and j!=0):
			q.put(ls)
			ls = []
	q.put(ls)	
	q.put("end")	
	return 0
	# print(ptext, os.getpid())


if __name__=='__main__':

	sys.stdout.write('\n\033[33m PARALLEL: Running... \n\n\033[0m')
	sys.stdout.flush()
	
	try:
		print("\t Generating ", format(combitn,',d'), "combinations...\n")
		print( "\t\t <", charlist, ">")
		startTime=dt.datetime.now()
		q=mp.Queue()
		with open(outfile,'w') as f:
			try:
				with mp.Pool(cores) as pool:
					
					result = pool.imap_unordered( functools.partial(gen_text, charlist=charlist, charlen=charlen), prefix_char )
					k=0
					que=[]
					procfin = 0 
					while (1):
						try:
							que = q.get(timeout=0.0001)
							if que == "end":
								procfin += 1
								que = []
								continue
							k += len(que)							
							f.write( '\n'.join( que ))
							f.write("\n")
	
							if procfin>=(len(prefix_char)-1):
								f.close()
								print("\n\n\t [+] All processes completed")
								break
						except Exception as e:
							pass

				q.close()
				pool.join()
				pool.close()
				f.close()
				os.rename(namefile,namefile[8:])
				print("\n\t Generated {:,d} phrases".format(k) ) 
				
			except Exception as e:
				print("\n### Entered exception ###")
				print(e)
				pass

		timeTaken = (dt.datetime.now() - startTime)
		minDuration = timeTaken/dt.timedelta(seconds=60)
		print("\n\t Total time taken",
				" \n\t\t minutes:", format(minDuration,  '.3f'),
				" \n\t\t seconds:", format( timeTaken.total_seconds(), '.3f' ),
				"\n\t\t rate   :", format(  k/(timeTaken.total_seconds()*10**6), '.5f' ), "million phrases per second")
                
		sys.stdout.write('\n\n\033[33m ### DONE ### \n\n\n\033[0m')

	except KeyboardInterrupt:
		pool.join()
		pool.close()
		f.close()
		sys.stdout.write('\033[33m') #terminal colour
		sys.stdout.write('\n User Interrupt \n')
#		print("Killed at", k, que[-1])
		sys.stdout.write('\033[0m')	#reset color
