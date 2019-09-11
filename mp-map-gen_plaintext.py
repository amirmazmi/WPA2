#!/usr/bin/env python3
#
# This script will generate permutations of possible plaintext passphrases
# for specific passphrase length
#
#	 - attemps to use all cores
#	- pool.map - wait for everything to finish
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
cores = mp.cpu_count()

#generate plaintext - small subset since too much time to calculate hash
charlen = 7
charlist = string.ascii_uppercase[:9]
prefix_char = string.ascii_lowercase		# pass a prefix to each process
combitn = (len(charlist)**charlen)*len(prefix_char)       #formula is length ^characters

#-----------------------------------------------------------------------------------------------------------------------------
pathfile = os.getcwd()
namefile = 'RUNNING-' + 'mp1-' + str(charlen+1) + '-char-plaintext.txt'
outfile = os.path.join(pathfile,namefile)

#-----------------------------------------------------------------------------------------------------------------------------
# wpa_passphrase cannot handle quotes
#  !#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
#-----------------------------------------------------------------------------------------------------------------------------

# generator function
def comb_gen( charlen, charlist):
		return itertools.product(charlist,repeat=charlen)


# function to join the combinations
def gen_text( prechar, charlen, charlist):
	li = []
	for i in comb_gen(charlen, charlist):
		li.append(''.join( (prechar,)+ i))
	return li
#	print(ptext, os.getpid())


if __name__=='__main__':

	sys.stdout.write('\n\033[33m PARALLEL: Running... \n\n\033[0m')
	sys.stdout.flush()

	try:
		print("\t Generating {:,d} combinations...\n".format(combitn) )
		print("\t expecting to take {:.3f} seconds\n".format(combitn/(1.7*10**6) ) )
		startTime = dt.datetime.now()
		with open(outfile,'w') as f:
			try:
				with mp.Pool(cores) as pool:
					result = pool.map( functools.partial(gen_text, charlist=charlist, charlen=charlen), prefix_char)
				pool.join()
				pool.close()
				outcome = list( itertools.chain.from_iterable(result) )
				# print(result, "\n")
				f.write( '\n'.join(outcome))
				f.write('\n')

			except queue.Empty:
				f.write('\n'.join(result))
				f.write('\n')
				# print("\n\n\t Exiting while loop")
				# break

		# q.close()
		# pool.join()
		# pool.close()
		# f.close()
		os.rename(namefile,namefile[8:])

		# print("\n\t Generated",format(k, ',d'), "phrases")

		timeTaken = (dt.datetime.now() - startTime)
		minDuration = timeTaken/dt.timedelta(seconds=60)
		print("\n\t Total time taken",
				" \n\t\t minutes:", format(minDuration,  '.3f'),
				" \n\t\t seconds:", format( timeTaken.total_seconds(), '.3f' ),
				"\n\t\t rate   :", format(  len(outcome)/(timeTaken.total_seconds()*10**6), '.3f' ), "million phrases per second")

		sys.stdout.write('\n\n\033[33m ### DONE ### \n\n\n\033[0m')

	except KeyboardInterrupt:
		pool.join()
		pool.close()
		sys.stdout.write('\033[33m') #terminal colour
		sys.stdout.write('\n User Interrupt \n')
		# print("Killed at", k, que[-1])
		sys.stdout.write('\033[0m')	#reset color
