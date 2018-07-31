var router = require('express').Router();
var db = require('./db.js');
var crypto = require('./cryptography.js');
var utils = require('./utils.js');

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
    //Comprobar formato de transacción
    format_err = utils.checktransactionformat(json)
    if (!format_err.correct)
        res.send("Bad format: " + format_err.msg);
    else{
        //Validar la firma
        crypto.validate_transaction(json, (err) => {
            if (err)
                res.send("Bad sign");
            else{
                //Añadir a la base de datos
                json["data"] = JSON.stringify(json["data"], null, 0);
                db.newtransaction(json);
                res.send("OK");
            }
        });
    }
});

module.exports.router = router;