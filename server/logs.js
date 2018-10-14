/*

    File name: logs.js
    Author: MathIsSimple
    Using: Nodejs
    Type: Build
    Build Version: 0.7
    Disclaimer: I created this project to learn about custom encoding and python sockets,
                this projected isn't made to be used for maliscious intent. Do so at your own risk

*/

const fs       = require('fs');
const readline = require('readline');

const LOGS  = "./../logs/";

if (fs.existsSync(LOGS) == false) {
    fs.mkdirSync(LOGS);
}

fs.readdir(LOGS, (err, logs) => {
    if (err) {
        throw err;
    }
    console.log("");
    console.log("The Logs Are : ");
    console.log("");
    for (log of logs) {
        console.log("    "+log);
    }
    console.log("");
    ask("Wich Log Do You Want To Open : ", (log) => {
        fs.readFile(LOGS + log, (err, data) => {
            if (err) {
                throw err;
            }

            console.log("");

            data = JSON.parse(data);
            info = data.info;

            for (el of info) {
                console.log(el);
            }

            console.log("");

            for (let i = 0; i < data.commands.length; i ++) {
                console.log(data.commands[i]);
                console.log("");
                for (let j = 0; j < data.responses[i].length; j ++) {
                    console.log(data.responses[i][j]);
                }
                console.log("");
            }

        });
    });
});

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