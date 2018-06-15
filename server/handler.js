var router = require('express').Router();
var db = require('./db.js');
var crypto = require('./cryptography.js');

router.post('/new_transaction', function(req, res) {
    res.send("Post received.");
});

router.post('/register', function(req, res) {
    //Falta variable para controlar si el registro está abierto o cerrado
    var json = req.body;
    //Comprobar formato del objeto recibido
    if (!json.hasOwnProperty("name") || typeof json["name"] != 'string' ||
        !json.hasOwnProperty("key") || typeof json["key"] != 'string')
        res.send("Bad format");
    else
        db.newkey(json["name"], crypto.create_hash(json["key"]), json["key"],
        (err) => {
            //TODO mejorar tratamiento de errores
            if(err)
                res.send("Database error.");
            else
                res.send("OK");
        });
});

module.exports.router = router;