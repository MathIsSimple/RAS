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

log_dir = "./../logs/"

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