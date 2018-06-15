#!/usr/bin/python

#################################################################
#
# zabbix-docker-stats.py
#
#   A program that produces information for Zabbix to
#   process Docker container statistics.
#
# Version: 1.0
#
# Author: Richard Sedlak
#
#################################################################

import sys
import subprocess
import os
import time

def B(b):
	return int(float(b))
	
def KB(b):
	return int(float(b) * 1024)
	
def MB(b):
	return int(float(b) * 1024 * 1024)

def GB(b):
	return int(float(b) * 1024 * 1024 * 1024)
	
def TB(b):
	return int(float(b) * 1024 * 1024 * 1024 * 1024)

size_options = {
	'k':KB,
	'K':KB,
	'm':MB,
	'M':MB,
	'g':GB,
	'G':GB,
	't':TB,
	'T':TB,
	'b':B,
	'B':B
}	


def pcpu(data):
	pdata=data.split()
	pcpu_data = pdata[2].split('%')[0]
	return pcpu_data

def umem(data):
        pdata=data.split()
#        umem_data = pdata[3].split('%')[0]
	return pdata[3][0]+pdata[3][1]+pdata[3][2]+pdata[3][3]

def lmem(data):
	pdata=data.split()
#	lmem_data = pdata[5].split('%')[0]
	return float(pdata[5][0]+pdata[5][1]+pdata[5][3])

def pmem(data):
	pdata=data.split()
	pmem_data = pdata[6].split('%')[0]
	return pmem_data

def inet(data):
	pdata=data.split()
	return pdata[7][0]+pdata[7][1]+pdata[7][2]+pdata[7][3]

def onet(data):
	pdata=data.split()
	return pdata[9][0]+pdata[9][1]+pdata[9][2]+pdata[9][3]

options = {
	'pcpu':pcpu,
	'umem':umem,
	'lmem':lmem,
	'pmem':pmem,
	'inet':inet,
	'onet':onet
}

def local_run_command(cmd,file):
	cmd = cmd + " | tee > " + file 
	if os.path.isfile(file) == False:
		os.system(cmd)
	else:
		(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
		ticks=int(time.time())
		delta=ticks-mtime
		if (delta > 60):
			os.system(cmd)

	strings = open(file,"r").readlines()
	return strings


container=sys.argv[1]
key=sys.argv[2]

cmd="docker stats --no-stream=true " + container
strings = local_run_command(cmd,"/tmp/zabbix-docker-stats-"+container+".out")

print options[key](strings[1])


