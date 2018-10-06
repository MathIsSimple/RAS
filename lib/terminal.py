#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: terminal.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Import core python needed modules

from subprocess import Popen
from subprocess import PIPE

# Lib Functions

def decodeCommandOutput(output):
    output = output.replace("\\", "/").replace("//", "/")
    output = output.replace("b'", "").replace('b"', "")
    output = output.replace("/r", "").replace("/n", "")
    output = output.replace("/x82", "é").replace("/x8a", "è")
    output = output.replace("/xff", " ")

    return output

def getCommandOutput(data):
    out = []
    process = Popen(data, stdout=PIPE, stderr=None, shell=True)

    while True:
        line = process.stdout.readline()

        if line != b"":
            contents = decodeCommandOutput(str(line))
            if contents.endswith("'") or contents.endswith('"'):
                contents = contents[:-1]
            if contents != "":
                if contents[0] == " ":
                    contents = contents[1:]
            out.append(contents)
        else:
            break
    
    out.append("END")
    return out