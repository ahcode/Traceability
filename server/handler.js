var router = require('express').Router();
var db = require('./db.js');
var crypto = require('./cryptography.js');
var utils = require('./utils.js');

router.post('/register', function(req, res) {
    if (utils.get_config_variable('register_opened')){
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
        var promise = new Promise((s) => {s();});
        //Comprobar que exista el receptor
        if (json.hasOwnProperty('receiver')){
            promise = promise.then(function(){ return db.check_key(json.receiver); })
            .catch(function(){ throw 'Receiver key does not exist or is not active'});
        }
        //Comprobar que el nuevo id esté disponible
        if (json.data.hasOwnProperty('new_id')){
            promise = promise.then(function(){ return db.check_available_id(json.data.new_id); })
            .catch(function(){ throw 'New id is duplicated'});
        }
        //Validar la firma
        promise.then(function(){
            return crypto.validate_transaction(json).then(function(){
                db.newtransaction(json).then(function(){utils.update_inputs(json)});
                res.send({'status': 'OK'});
            });
        }).catch(function(msg){res.send({'status': 'ERROR', 'error': msg})});
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
        res.send({'status': 'ERROR', 'error': 'Incorrect format'});
    }
});

router.post('/get_register_status', function(req, res){
    json = req.body;
    if(json.hasOwnProperty('config_key') && json.config_key == process.env.REMOTE_CONFIG_KEY){
        var r = utils.get_config_variable('register_opened');
        if(r) res.send({'status': 'OK', 'remote_register': 'on'});
        else res.send({'status': 'OK', 'remote_register': 'off'});        
    }else{
        res.send({'status': 'ERROR', 'error': 'config_key is not correct'});
    }
});

router.post('/set_register_status', function(req, res){
    json = req.body;
    if(json.hasOwnProperty('config_key') && json.config_key == process.env.REMOTE_CONFIG_KEY){
        if(json.hasOwnProperty('remote_register') && (json.remote_register == 'on' || json.remote_register == 'off')){
            if(json.remote_register == 'on')
                utils.set_config_variable('register_opened', true);
            else
                utils.set_config_variable('register_opened', false);
            res.send({'status': 'OK'})
        }else{
            res.send({'status': 'ERROR', 'error': 'remote_register must be \'on\' or \'off\''})
        }
    }else{
        res.send({'status': 'ERROR', 'error': 'config_key is not correct'})
    }
});

module.exports.router = router;