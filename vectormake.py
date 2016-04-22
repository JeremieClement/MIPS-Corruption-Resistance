#!/usr/bin/python
#!coding=latin1
import os
'''
Generates the Vector for a MIPS program to protect it from
alterations.
Example based on a three lock verification. More locks can be added
Author: Jeremie CLEMENT
'''
#Input program
try:
	fichier = open("InputP.hex","r")
except Exception, message:
	print message
#Output program + vector
try:
	ofic = open("testvector.hex","w")
except Exception, message:
	print message
#Arbitrarily chosen constants (1 for each desired lock)
cst1 = '0x12345678'
cst2 = '0x9ABCDEF0'
#address where will be written the third lock for verifications by the program in memory (8 bits)
addr = '0x11342222'
#Definition of the lock variables
b = ''
c = ''
#Defines the size of the program P
endoffset = len(fichier.readlines())-4
fichier.seek(0, os.SEEK_SET)
#Put the constants first
vector = "3C01"+cst1[2:6]+"\n342A"+cst1[6:10]+"\n3C01"+cst2[2:6]+"\n342B"+cst2[6:10]+"\n"
#Start address of the first instruction to be verified
startaddr = "0x0040003C"
#The start of the verification (don't forget twice)
vector += "3C01"+startaddr[2:6]+"\n3434"+startaddr[6:10] + "\n"
#The end address (39 is the number of instructions in V since startaddr)
totalsize = int(startaddr, 16) + ((endoffset + 4 + 39) -1) * 4 
totalS = '0'*(8-len(hex(totalsize)[2:])) + hex(totalsize)[2:]
vector +="3C01" + totalS[2:6] + "\n3435" + totalS[6:10] + "\n0000b020\n"
#Adding The multiplicative constant
phi = '0x9E3779B1'
vector +="3C01"+phi[2:6]+"\n342f"+phi[6:10]+"\n"
#The checksum calculation function
#Each instruction is preceeded with a double verification of the instruction
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef0007c\n3c118e89\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef0007c\n3c118e89\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="8e890000\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef000d8\n3c01010f\n34310019\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef000d8\n3c01010f\n34310019\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="010f0019\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef0012c\n34114012\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef0012c\n34114012\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="00004012\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef00188\n3c010109\n34314021\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef00188\n3c010109\n34314021\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="01094021\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef001e4\n3c012294\n34310004\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef001e4\n3c012294\n34310004\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="22940004\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef00240\n3c011695\n3431ff7b\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef00240\n3c011695\n3431ff7b\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="1695ff7b\n"
#First lock Verification
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef0029c\n3c010113\n34319826\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="3c01" + startaddr[2:6] +"\n3437" + startaddr[6:10] +"\n8ef0029c\n3c010113\n34319826\n02309022\n34027fff\n3042000a\n34110001\n0232100a\n0000000c\n"
vector +="01139826\n"
vector +="34027fff\n3042000a\n34110001\n0233100a\n0000000c\n"
#Second lock verification
vector +="010A4021\n010d6826\n"
vector +="34027fff\n3042000a\n34110001\n022d100a\n0000000c\n"
#Third lock verification
vector +="010B4021\n"
#Store of the verification value used inside the program to avoid jumps
vector +="3C0F" + addr[2:6] + "\n35EF" + addr[6:10] +"\nADE80000\nADEE0004\n010E7026"
vector +="34027fff\n3042000a\n34110001\n022e100a\n0000000c\n"
ofic.write(vector)
#Write it in a file
while 1:
    ligne = fichier.readline()
    if not ligne : break
    ofic.write(ligne)
fichier.close()
ofic.close()

#Calculation of the expected checksum based on an alternation of additions and Xors
try:
	ofic = open("testvector.hex","r")
except Exception, message:
	print message
chk = 0
multi = int('9E3779B1', 16)
while 1:
    ligne = ofic.readline()
    if not ligne : break
	chk = chk * multi
    chk = chk & int('FFFFFFFF', 16)
	chk = chk + int(ligne, 16)
	chk = chk & int('FFFFFFFF', 16)
check = '0'*(8-len(hex(chk)[2:-1])) + hex(chk)[2:-1]
verifvector = "3C13" + check[:4] + "\n3673" + check[4:] + "\n"
#Second lock value calculation
b = int(check, 16) + int(cst1, 16)
b = b & int('FFFFFFFF', 16)
verifvector += "3C01" + hex(b)[2:6] + "\n342D" + hex(b)[6:10] + "\n"
#Third lock value calculation
c = b + int(cst2, 16)
c = c & int('FFFFFFFF', 16)
verifvector += "3C01" + hex(c)[2:6] + "\n342E" + hex(c)[6:10] + "\n"
#Write into the final file
try:
	fichier = open("outputP.hex","w")
except Exception, message:
	print message

fichier.write(verifvector)
ofic.seek(0, os.SEEK_SET)
while 1:
    ligne = ofic.readline()
    if not ligne : break
    fichier.write(ligne)
fichier.close()
ofic.close()
			
