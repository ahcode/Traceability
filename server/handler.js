var router = require('express').Router();
var db = require('./db.js');
var crypto = require('./cryptography.js');
var utils = require('./utils.js');

router.post('/register', function(req, res) {
    if (true){ //FALTA COMPROBAR SI EL REGISTRO ESTÁ ABIERTO
        var json = req.body;
        //Comprobar formato del objeto recibido
        if (!utils.checkregisterformat(json))
            res.send("Bad format");
        else
            //Añadir a la base de datos
            db.newkey(json.name, crypto.create_hash(json.key), json.key)
            .then(function(){res.send("OK")}, function(msg){res.send(msg)});
    }else{
        res.send("Server is not accepting new keys");
    }
});

router.post('/newtransaction', function(req, res) {
    var json = req.body;
    //Comprobar formato de transacción
    var format_err = utils.checktransactionformat(json)
    if (!format_err.correct)
        res.send("Bad format: " + format_err.msg);
    else{
        //Validar la firma
        crypto.validate_transaction(json).then(function(){
            db.newtransaction(json).then(function(){utils.update_inputs(json)}); //TODO
            res.send("OK");
        },
        function(msg){
            res.send(msg);
        });
    }
});

router.get('/version', function(req, res) {
    var ver = require('./package.json').version;
    res.send({'version': ver})
});

router.post('/keycheck', function(req, res){
    json = req.body;
    if(json.hasOwnProperty('key')){
        db.check_key(json['key']).then(function(){
            res.send({'status': 'OK'});
        }, function(){
            res.send({'status': 'ERROR', 'error': 'Key is not registered or activated.'});
        });
    }else{
        res.send({'status': 'ERROR', 'error': 'Bad format'})
    }
});

module.exports.router = router;