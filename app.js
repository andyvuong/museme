var osc = require("node-osc"),
    http = require("http"),
    WebSocket = require("ws");
var ajax = require('ajax');
var express = require('express');
var fs = require('fs');
//var processing = require('processing-js');

// App begins
var app = express();
var routes  = require('./routes/index.js');
app.use(express.static(__dirname + '/public'));
app.use("/public", express.static(__dirname + '/styles'));
 
// Wolfram  base
var base = 'https://www.wolframcloud.com/objects/37e0b60d-f828-4613-95e0-12a2c5aa1314';

// Globals
var port_running = 3000;
var port_osc = 2000;
var val = [];
var rang = [];

// New OSC client that 
var client = new osc.Client('127.0.0.1', port_osc);
client.send('/oscAddress', 200);

// Osc client 
var oscServer = new osc.Server(port_osc, '0.0.0.0');

/**
* Listens for incoming OSC messages.
*/
function listen() {
oscServer.on("message", function (msg, rinfo) {
      console.log("OSC Message:");
      console.log(msg);
      val.push(msg[1]);


      process(val); // pass values to graph
      //process1(val); // pass values to chuck
      //process2(); // pass values to music
});}

/**
* Processes the incoming values for the brain wave graph
*/
function process(item) {
    if(item.length > 10) {
        // do something with the array values

        val = [];
    }
}

/**
* Processes the incoming values for emotions and subsequently music, visualization, and color changing
*/
function process(item) {
    if(item.length > 10) {
        // do something with the array values

        val = [];
    }
}

// Communicate between server and front-end



// Start server
listen();
// "Front-facing" server
console.log("Express server running on " + port_running);
console.log("OSC server listening on " + port_osc);
app.listen( port_running);
