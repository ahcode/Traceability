var express = require("express");
var app = express();
var bodyParser  = require("body-parser");
var handler = require("./handler.js");
var fs = require("fs");
var https = require("https");
var http = require("http");

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(handler.router);

if(process.env.NODE_HTTPS == "TRUE"){
  var privateKey  = fs.readFileSync(process.env.SSL_KEY, 'utf8');
  var certificate = fs.readFileSync(process.env.SSL_CRT, 'utf8');
  var credentials = {key: privateKey, cert: certificate};
  server = https.createServer(credentials, app);
}else{
  server = http.createServer(app);
}

server.listen(parseInt(process.env.SERVER_PORT), function() {
  console.log("Traceability server running...");
});