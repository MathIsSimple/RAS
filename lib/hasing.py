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

bits_per_char = len(bin(len(characters))) - 2

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