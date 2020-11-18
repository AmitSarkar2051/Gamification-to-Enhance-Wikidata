import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import os
import shutil

def create_PropMapFile(myList,mapFile):
    print("Writing in the  MAP file")
    print("Available size", len(myList))
    with open(mapFile, 'w') as f:
        for item in myList:
            f.write("%s\n" % item)

if(len(sys.argv)<2):
    print("Number of argument required is 2. \nFormat: python3 <progname>.py <lang>")
    exit(1)
LN = sys.argv[1]

#global vars
hnFile="ALL_"+LN+"_proplist.txt"
enFile="ALL_en_proplist.txt"
mapFile="map_proplist_"+LN+".txt"

fhn = open(hnFile, 'r')
fen = open(enFile, 'r')

hnlines = [line for line in fhn.readlines()]
enlines = [line for line in fen.readlines()]
maplines = []

for i in range(len(hnlines)):
    hnlabel=hnlines[i].strip().strip('\n')
    enlabel=enlines[i].strip().strip('\n')
    if(hnlabel[0] == 'P'):
        maplines.append(hnlabel+","+enlabel)
        #print(hnlabel+","+enlabel)

create_PropMapFile(maplines,mapFile)
print("Map file created successfully. Please Check: ",mapFile)



