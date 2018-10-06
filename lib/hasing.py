#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: hasing.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# All the supported charachters of the program

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/;:.,éè'\?!&+*|`^@[]=#~-_<>(){}§\"$%µ£¤ç "

def modify(message):
    output = ""

    for l in message:
        index  = characters.find(l)
        index2 = len(characters) - 1 - index
        letter = characters[index2]
        output = output + letter
    
    return output