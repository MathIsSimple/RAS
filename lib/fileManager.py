#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: fileManager.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Import needed core python modules

from os import walk
from os import path

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