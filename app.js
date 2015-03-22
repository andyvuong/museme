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
var val_alpha_r = [];
var val_beta_r = [];
var val_delta_r = [];
var val_theta_r = [];
var val_gamma_r = [];
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
      console.log(typeof JSON.stringify(msg));
      parsed = JSON.stringify(msg).split(" ");
      console.log(parsed.length);
      path =  parsed[0];
      // PARSE CODE -> Push the average of the respective wave//
      if(path.localeCompare("/muse/elements/delta_absolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_delta.push(parsed[i]);
          }
      }
      else if (path.localeCompare("/muse/elements/theta_absolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_theta.push(parsed[i]);
          }
      }
      else if (path.localeCompare("/muse/elements/alpha_absolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_alpha.push(parsed[i]);
          }
       }
      else if (path.localeCompare("/muse/elements/beta_absolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_beta.push(parsed[i]);
          }
       }
      else if (path.localeCompare("/muse/elements/gamma_absolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_gamma.push(parsed[i]);
          }
       } /////
      else if (path.localeCompare("/muse/elements/delta_resolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_delta_r.push(parsed[i]);
          }
       }
      else if (path.localeCompare("/muse/elements/theta_resolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_theta_r.push(parsed[i]);
          }
       }
      else if (path.localeCompare("/muse/elements/alpha_resolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_alpha_r.push(parsed[i]);
          }
       }
      else if (path.localeCompare("/muse/elements/beta_resolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_beta_r.push(parsed[i]);
          }
       }
      else if (path.localeCompare("/muse/elements/gamma_resolute")) {
          for(var i = 1; i < parsed.length; i++) {
              val_gamma_r.push(parsed[i]);
          }
       }
       else {
              console.log("Something weird happened!");
       }
       console.log(msg);
       console.log(parsed);
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
