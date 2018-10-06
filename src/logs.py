#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: logs.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Import needed core python modules

from sys import path

path.insert(0, './../lib/')

# Import needed custom python modules

from hasing      import decrypt
from fileManager import getFilesInDir
from fileManager import getFileExtension
from fileManager import fileExists

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