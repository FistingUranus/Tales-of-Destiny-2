import os.path
import json
import subprocess
import shutil
import itertools
import pandas as pd
import pygsheets
import re

def parseText(fileName):
    
    fread = open(os.path.join(os.getcwd(),"abcde", fileName),encoding="utf-8", mode="r")
    lines = fread.readlines()
    
    start=0
    end=0
    mylist=[]
    dfLines = pd.DataFrame(lines, columns=["Text"])
    finalList=[]
    
    for i,line in enumerate(lines):
        
        if "//Text " in line:
            start=i
        if "// current" in line:    
            finalList.append("".join(dfLines['Text'][start:i]))
    
    return finalList

def writeColumn(finalList, googleId):
    
    gc = pygsheets.authorize(service_file=os.path.join("MenuScripts","BaseScripts","gsheet.json"))
    sh = gc.open_by_key(googleId)

    #Look for Dump sheet 
    wks = sh.worksheet('title','Dump')
    
    
    #update the first sheet with df, starting at cell B2. 
    df=pd.DataFrame({"Japanese":finalList, "English":finalList})
    wks.set_dataframe(df,(1,0))

def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

def cleanData(dfData):
    dfData['English'] = dfData['English'].apply(lambda x: re.sub('\[END]$', '[END]\n', x))
    dfData['English'] = dfData['English'].str.replace("\r","")
    dfData['English'] = dfData['English'].str.replace("\r","")
    return dfData


googleId = '15cX1Vb6jsnoev4T3o-x00jYNaNgNdz6h2QwApBocjQg'
fileName = 'TOD2_SideMenu_Dump_cleaned.txt'
finalList = parseText(fileName)
writeColumn(finalList, googleId)
    
