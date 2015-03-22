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
 
//
// Globals
var port_running = 3000;
var port_osc = 5003;
var val_alpha = [];
var val_beta = [];
var val_delta = [];
var val_theta = [];
var val_gamma = [];
var rang = [];

// New OSC client that 
var client = new osc.Client('localhost', port_osc);
//client.send('/oscAddress', 200);

// Osc server
var oscServer = new osc.Server(port_osc, '0.0.0.0');

/**
* Listens for incoming OSC messages.
*/
function listen() {
oscServer.on("message", function (msg, rinfo) {
      console.log("OSC Message:");
      console.log(msg);
      parsed = msg.split(" ");

      path =  parsed[0];
      // PARSE CODE -> Push the average of the respective wave//
      if(path.localeCompare("/muse/elements/delta_absolute")) {
          for(var i = 1; i < len(parsed); i++) {
              val_delta.push(parsed[i]);
          }
      }
      else if (path.localeCompare("/muse/elements/theta_absolute")) {
          for(var i = 1; i < len(parsed); i++) {
              val_theta.push(parsed[i]);
          }
      }
      else if (path.localeCompare("/muse/elements/alpha_absolute")) {
          for(var i = 1; i < len(parsed); i++) {
              val_alpha.push(parsed[i]);
          }
       }
      else if (path.localeCompare("/muse/elements/beta_absolute")) {
          for(var i = 1; i < len(parsed); i++) {
              val_beta.push(parsed[i]);
          }
       }
      else if (path.localeCompare("/muse/elements/gamma_absolute")) {
          for(var i = 1; i < len(parsed); i++) {
              val_gamma.push(parsed[i]);
          }
       }
       else {
              console.log("Something weird happened!");
       }
      //  Passes each of the 4 channels for each wave
      process(val_delta, val_theta, val_alpha, val_beta, val_gamma); 
      //process1(val); // pass values to chuck
      //process2(); // pass values to music
});}


/**
* Processes the incoming values for emotions and subsequently music, visualization, and color changing
*/
function process(item1, item2, item3, item4, item5) {
    if(item1.length > 5) {
      // do something with 5 averaged values from the previous function right here:
      // calculate a mood
////
      // 1 - music generation
      // Pass all 5 values
      // needs to return 3 cords and a melodynote

      // 2 - pass to the visualization
      //  chord1 chord2 chord3 melodynote 
      // mood
      // communicate




      // resets the global variable to empty arrays
      val_delta = [];
      val_theta = [];
      val_alpha = [];
      val_beta = [];
      val_gamma = [];
    }
}



// Start server
listen();
// "Front-facing" server
console.log("Express server running on " + port_running);
console.log("OSC server listening on " + port_osc);
app.listen( port_running);
:wq
