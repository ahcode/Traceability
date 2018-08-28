var express = require("express");
var app = express();
var bodyParser  = require("body-parser");
var handler = require("./handler.js");

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(handler.router);

app.listen(parseInt(process.env.SERVER_PORT), function() {
  console.log("Traceability server running...");
});