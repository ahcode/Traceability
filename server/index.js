var express = require("express");
var app = express();
var bodyParser  = require("body-parser");
var handler = require("./handler.js");

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(handler.router);

app.listen(8080, function() {
  console.log("Trazability server running...");
});