#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: logs.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Type: Build
    Build Version: 0.6b
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Importing

from os import walk
from os import path

# Global Variables

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/;:.,éè'\?!&+*|`^@[]=#~-_<>(){}§\"$%µ£¤ç "
bits_per_char = len(bin(len(characters))) - 2

# Hasing Functions

def modify(message):
    output = ""

    for l in message:
        index  = characters.find(l)
        index2 = len(characters) - 1 - index
        letter = characters[index2]
        output = output + letter
    
    return output

def longify(message):
    output = ""
    for char in message:
        bin_number = str(bin(characters.find(char)))[2:]
        for i in range(bits_per_char - len(bin_number)):
            bin_number = "0" + bin_number
        output = output + bin_number
    return output

def delongify(message):
    output = ""
    for i in range(int(len(message) / bits_per_char)):
        char   = int(message[i * bits_per_char:i * bits_per_char + bits_per_char], 2)
        output = output + characters[char]
    return output

def encrypt(message):
    output = modify(message)
    output = output[::-1]
    output = longify(output)
    return output

def decrypt(message):
    output = delongify(message)
    output = output[::-1]
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

print("Open Logs")

log_dir = "./logs/"

def start():
    logs = getFilesInDir(log_dir)

    for log in logs:
        print("Log File : " + log)

    log_to_open = input("File to Open : ")
    print("")
    if log_to_open == "END":
        exit(0)
    extension   = getFileExtension(log_to_open)

    if extension != ".txt":
        log_to_open = log_to_open + ".txt"

    log_to_open_location = log_dir+log_to_open

    if fileExists(log_to_open_location):
        f = open(log_to_open_location, "r")
        print("Opened log")

        while True:
            line = f.readline().replace("\n", "").replace("\r", "")
            if line == "": break
            print(decrypt(line))
        
        f.close()
    else:
        print("This log doesn't exist")
    print("")
    start()
start()