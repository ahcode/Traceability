var router = require('express').Router();
var db = require('./db.js');
var crypto = require('./cryptography.js');
var utils = require('./utils.js');

router.post('/new_transaction', function(req, res) {
    res.send("Post received.");
});

router.post('/register', function(req, res) {
    //Falta variable para controlar si el registro está abierto o cerrado
    var json = req.body;
    //Comprobar formato del objeto recibido
    if (!utils.checkregisterformat(json))
        res.send("Bad format");
    else
        //Añadir a la base de datos
        db.newkey(json["name"], crypto.create_hash(json["key"]), json["key"],
        (err) => {
            //TODO mejorar tratamiento de errores
            if(err)
                res.send("Database error.");
            else
                res.send("OK");
        });
});

router.post('/newtransaction', function(req, res) {
    var json = req.body;
    if (!utils.checktransactionformat(json))
        res.send("Bad format");
    else if(!crypto.validate_transaction(json))
        res.send("Bad sign");
    else{
        //Añadir a la base de datos
        if (json.hasOwnProperty("receiver"))
            var receiver = json["receiver"];
        else
            var receiver = null;
        db.newtransaction(json["hash"], json["type"], json["transmitter"], receiver, json["timestamp"], json["data"], json["sign"],
        (err) => {
            //TODO mejorar tratamiento de errores
            if(err)
                res.send("Database error.");
            else
                res.send("OK");
        });
    }
});

module.exports.router = router;