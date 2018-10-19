# Warning 

I have created this project to learn about custom encoding and python sockets, this projected isn't made to be used with maliscious intent and should be used in my opinion like ssh is.

Only use this on your own computer(s) or with authorisation!

# INFO

Made by MathIsSimple
Made to be used along with ssh

# Instructions

### How to instal : 

+ Install git [From this link](https://git-scm.com/)
+ install python3 [From this link](https://www.python.org/)
+ Install pygame (for the gui)
    ```
    pip install pygame
    ```
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
+ Open the server
+ Open one or more clients

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
+ The client sends every 0.05s a piece of information to server, when all of the information has been sent, the client sends "END" to server to let it know that it can now send commands to it
+ The client now waits for commands comming from the server
+ When it gets a command, it gets the command's output and adds END at the end to let the server know that the transmission has ended and it can now continue sending commands
+ If the client recieves the command "END" it will shutdown and the server will write a log in the logs directory
+ If there were to be a disconnect, the client will try every 5s to reconnect

If you have any questions, ask me!

Made with passion for programming!
