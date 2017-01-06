#!/usr/bin/env python

import numpy as np
import argparse
import math
from argparse import RawTextHelpFormatter,SUPPRESS

parser = argparse.ArgumentParser(description='''Finds minimum value of a data file''',formatter_class=RawTextHelpFormatter)

parser.add_argument('-l', help ="Liquid File Name")
parser.add_argument('-v', help ="Vapor File Name")
parser.add_argument('-b', help ="Number of Blocks")
parser.add_argument('-s', help ="How to divide the file")
args = parser.parse_args()
file1name=args.l
block=int(args.b)
skip=int(args.s)
file1 = open(file1name)
file1.readline()
line1=file1.readline()
line1 = line1.split()
file1.close()

file2name=args.v
file2 = open(file2name)
file2.readline()
line2=file2.readline()
line2 = line2.split()
file2.close()

fmt1 = '%15.6f'
fmt2 = '%15.6f'
fmt3 = '%15.6f'
fmt4 = '%15.6f'
data1 = np.loadtxt(file1name, skiprows=3)
data2 = np.loadtxt(file2name, skiprows=3)
print "Run Summary\n"
print "-----------\n"
avgfile="average.dat"
aout=open(avgfile,'w')
aout.write("number of blocks="+str(block)+"\n")
aout.write("number of skip="+str(skip)+"\n")
if block==0:
    for i in range(len(line1)-1):
        y_data_1 = data1[:,i]
        y_data1 = y_data_1[int(len(y_data_1)-len(y_data_1)/skip):]
        y_data_2 = data2[:,i]
        y_data2 = y_data_2[int(len(y_data_2)-len(y_data_2)/skip):]
        testname="blocktest_"+line1[i+1]+".dat"
        test=open(testname,'w')
        for b in range(1,40,1):
            y_data_block1 = np.split(y_data1[len(y_data1)%b:],b)
            y_data_block2 = np.split(y_data2[len(y_data2)%b:],b)
            avg_y_data_block1 = np.average(y_data_block1,1)
            avg_y_data_block2 = np.average(y_data_block2,1)
            test.write(str(b)+" "+str(np.average(avg_y_data_block1))+" "+str(np.std(avg_y_data_block1,ddof=1)/pow(b,0.5))+" "+str(np.average(avg_y_data_block2))+" "+str(np.std(avg_y_data_block2,ddof=1)/pow(b,0.5))+"\n")
        test.close()
else:        
    for i in range(len(line1)-1):
        outfile=line1[i+1]+".dat"
        f=open(outfile,'w')
        y_data_1 = data1[:,i]
        y_data1 = y_data_1[int(len(y_data_1)-len(y_data_1)/skip):]
        y_data_2 = data2[:,i]
        y_data2 = y_data_2[int(len(y_data_1)-len(y_data_2)/skip):]
        y_data_block1 = np.split(y_data1[len(y_data1)%block:],block)
        y_data_block2 = np.split(y_data2[len(y_data2)%block:],block)
        avg_y_data_block1 = np.average(y_data_block1,1)
        avg_y_data_block2 = np.average(y_data_block2,1)
        for m in range(0,block,1):
            f.write(str(avg_y_data_block1[m])+" "+str(avg_y_data_block2[m])+"\n")
        f.close()
        print line1[i+1],fmt1%np.average(avg_y_data_block1), fmt2%np.std(avg_y_data_block1,ddof=1), fmt3%np.average(avg_y_data_block2), fmt4%np.std(avg_y_data_block2,ddof=1)
        aout.write(str(line1[i+1])+" "+str(np.average(avg_y_data_block1))+" "+str(np.std(avg_y_data_block1,ddof=1))+" "+str(np.average(avg_y_data_block2))+" "+str(np.std(avg_y_data_block2,ddof=1))+"\n")
