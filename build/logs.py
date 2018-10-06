#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: logs.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Importing

from os import walk
from os import path

# Hasing Functions

def modify(message):
    output = ""

    for l in message:
        index  = characters.find(l)
        index2 = len(characters) - 1 - index
        letter = characters[index2]
        output = output + letter
    
    return output

def encrypt(message):
    output = modify(message)
    output = output[::-1]
    return output

def decrypt(message):
    output = message[::-1]
    output = modify(output)
    return output

# Lib Functions

def getFilesInDir(dir):
    files = []

    for (dirpath, dirnames, filenames) in walk(dir):
        files.extend(filenames)

    return files

def getFileExtension(f):
    return f[-4:]

def fileExists(f):
    return path.isfile(f)

def createWritableFile(loc):
    f = open(loc, "w+")
    return f

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/;:.,éè'\?!&+*|`^@[]=#~-_<>(){}§\"$%µ£¤ç "

print("Open Logs")
logs = getFilesInDir("./../logs/")

for log in logs:
    print("Log File : " + log)

log_to_open = input("File to Open : ")
extension   = getFileExtension(log_to_open)

if extension != ".txt":
    log_to_open = log_to_open + ".txt"

log_to_open_location = "./../logs/"+log_to_open

if fileExists(log_to_open_location):
    f = open(log_to_open_location, "r")
    print("Opened log")

    while True:
        line = f.readline().replace("\n", "").replace("\r", "")
        if line == "": break
        print(decrypt(line))
    
    f.close()
    exit(0)
else:
    print("This log doesn't exist")