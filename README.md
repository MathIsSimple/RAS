# RAS : Remote Acces Software

This project enables you to send commands to another pc and receive the output of that command remotly.
This also enables you transfer files

Made by MathIsSimple
Made to be used along with ssh

### Warning 

I have created this project to learn about custom encoding and python sockets, this projected isn't made to be used with maliscious intent and should be used in my opinion like ssh is.

Only use this on your own computer(s) or with authorisation!

### Features

+ Send and receive output of commands
+ Download files
+ Encryption for command output

# Instructions

### How to instal : 

+ Install git [From this link](https://git-scm.com/)
+ install python3 [From this link](https://www.python.org/)
+ Install requests (for the ip information)
    ```
    pip install requests
    ```
+ Clone the repository
    ```
    cd path/to/your/lococation/to/install
    git clone https://github.com/MathIsSimple/RAS.git
    ```
    
### How to use : 

+ Got to the exec folder
+ Go into win/ or linux (if you are on mac or linux)
+ If win/
	* Double click on server.bat and double click on client.bat in python/ or in python3/
+ IF linux/
	* Open the terminal and navigate to the linux/ folder
	* Go to python/ or python3/ and type sh start_server.sh
	* GO to python/ or python3/ and type sh start_client.sh
		
+ Once you are connected with a client, you can type HELP to get the list of supported commands and how to use them

# The protocol

+ The server boots up, and gets the config from res/config.json and aplies it.
+ It creates the numbers g and p for the [Diffie–Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)
+ It waits for a connection from a client on a port (can be changed in the config)
+ Before connecting, the client gathers information about the system it is running on
+ Then, the client connects to the server
+ It then does the [Diffie–Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)
    * The client is now always listening for data from the server
    * Step 1 :
        * The server sends to the client the number g and the client stores it
    * Step 2 :
        * The server sends to the client the number n and the client stores it
        * The client creates its p value
        * The client creates a new g value with all the information it has been sent
    * Step 3 :
        * The server sends to the client his new g value
        * The client calculates its key
        * The client sends its "new" g value
    * Step 4 :
        * The server calculates the key after recieving the client's "new" g value
+ After that, they prepare for the [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher) which will be used to encrypt and decrypt messages
    * The server and the client create a cipher with the numerical key that they both have getting all of the program's supported characters up to the key modulo the length of the supported characters
    * By this time, the server and the client have already created the Vigenère square
+ From now on, all communication will be encrypted
+ The encryption process is a bit more complicated but it is not worth mentioning because it could be removed
+ The server listens for the client's information
+ The client sends every 0.1s a piece of information to server, when all of the information has been sent, the client sends "END" to server to let it know that it can now send commands to it
+ The client now waits for commands comming from the server
+ When it gets a command, it gets the command's output and adds END at the end to let the server know that the transmission has ended and it can now continue sending commands
+ If there were to be a disconnect, the client will try every 5s to reconnect
+ The client opens a gui and a webserver thread, the webserver is used to transfer the files
+ If the server receives a command starting with open, it asks the client for the file
+ And the client responds with the file

# Change Logs

## Commit 37

+ Added executables for linux/mac

## Commit 36

+ Not Much

## Commit 35

+ Now handles errors without buging out or crashing!
+ you can download and upload files with spaces in them
+ There now is an init.bat file which removes the placeholder.txt files that are here to make so that git puts it in the repo
+ When you download a file from the client's computer, it now shows it's real name in you server/downloads/ folder
+ Removed the GUI because it had no purpose

If you have any questions or ideas, make a pull request or an issue.
