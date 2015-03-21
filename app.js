// Create an osc.js UDP Port listening on port 5000 . 
var udpPort = new osc.UDPPort({
    localAddress: "0.0.0.0",
    localPort: 57121
});
 
// Listen for incoming OSC bundles. 
udpPort.on("bundle", function (oscBundle) {
    console.log("An OSC bundle just arrived!", oscBundle);
});
 
// Open the socket. 
udpPort.open();
 
// Send an OSC message to, say, SuperCollider 
udpPort.send({
    address: "/s_new",
    args: ["default", 100]
}, "127.0.0.1", 57110);