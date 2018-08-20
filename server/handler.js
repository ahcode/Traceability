var router = require('express').Router();
var db = require('./db.js');
var crypto = require('./cryptography.js');
var utils = require('./utils.js');

router.post('/register', function(req, res) {
    if (true){ //FALTA COMPROBAR SI EL REGISTRO ESTÁ ABIERTO
        var json = req.body;
        //Comprobar formato del objeto recibido
        var fres = utils.checkregisterformat(json)
        if (fres.error)
            res.send({'status': 'ERROR', 'error': fres.error});
        else
            //Añadir a la base de datos
            db.newkey(json.name, crypto.create_hash(json.key), json.key)
            .then(function(){res.send({'status': 'OK'})}, function(msg){res.send({'status': 'ERROR', 'error': msg})});
    }else{
        res.send({'status': 'ERROR', 'error': "Server is not accepting new keys"});
    }
});

router.post('/newtransaction', function(req, res) {
    var json = req.body;
    //Comprobar formato de transacción
    var fres = utils.checktransactionformat(json)
    if (fres.error)
        res.send({'status': 'ERROR', 'error': "Incorrect format: " + fres.error});
    else{
        //Validar la firma
        crypto.validate_transaction(json).then(function(){
            db.newtransaction(json).then(function(){utils.update_inputs(json)}); //TODO
            res.send({'status': 'OK'});
        },
        function(msg){
            res.send({'status': 'ERROR', 'error': msg});
        });
    }
});

router.get('/version', function(req, res) {
    var pack = require('./package.json');
    res.send({'status': 'OK', 'version': pack.version, 'protocol_version': pack.protocol_version})
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
        res.send({'status': 'ERROR', 'error': 'Incorrect format'})
    }
});

module.exports.router = router;