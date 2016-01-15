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
	fichier = open("testtrans.hex","r")
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
#Definition of the lock variables
b = ''
c = ''
#Defines the end of the program P
endoffset = len(fichier.readlines())-4
fichier.seek(0, os.SEEK_SET)
#Put the constants first
vector = "3C0A"+cst1[2:6]+"\n354A"+cst1[6:10]+"\n3C0B"+cst2[2:6]+"\n356B"+cst2[6:10]+"\n"
#The start offset and verification (don't forget twice)
vector += "24040018\n24050018\n"
vector += "1485" + '0'*(4-len(hex(22+endoffset)[2:])) + hex(22+endoffset)[2:] + "\n"
vector += "00000000\n"
totalsize = ((endoffset + 4 + 35) -1) * 4
vector +="2405" + '0'*(4-len(hex(totalsize)[2:])) + hex(totalsize)[2:] + "\n24060000\n8C890000\n00000000\n"
#The checksum calculation function
vector +="01094020\n20840004\n10850007\n00000000\n8C890000\n00000000\n01094026\n20840004\n1485FFF5\n00000000\n"
#First lock Verification
vector +="1507" + '0'*(4-len(hex(6+endoffset)[2:])) + hex(6 + endoffset)[2:] + "\n"
#Second lock verification
vector +="00000000\n010A4020\n150D" + '0'*(4-len(hex(3+endoffset)[2:])) + hex(3+endoffset)[2:] + "\n"
#Third lock verification
vector +="00000000\n010B4020\n150E" + '0'*(4-len(hex(endoffset)[2:])) + hex(endoffset)[2:] + "\n"
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
while 1:
    ligne = ofic.readline()
    if not ligne : break
    chk += int(ligne, 16)
    chk = chk & int('FFFFFFFF', 16)
    ligne = ofic.readline()
    if not ligne : break
    chk = chk ^ int(ligne, 16)
check = '0'*(8-len(hex(chk)[2:-1])) + hex(chk)[2:-1]
verifvector = "3C07" + check[:4] + "\n34E7" + check[4:] + "\n"
#Second lock value calculation
b = int(check, 16) + int(cst1, 16)
b = b & int('FFFFFFFF', 16)
verifvector += "3C0D" + hex(b)[2:6] + "\n35AD" + hex(b)[6:10] + "\n"
#Third lock value calculation
c = b + int(cst2, 16)
c = c & int('FFFFFFFF', 16)
verifvector += "3C0E" + hex(c)[2:6] + "\n35CE" + hex(c)[6:10] + "\n"
#Write into the final file
try:
	fichier = open("testtrans.hex","w")
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
			
