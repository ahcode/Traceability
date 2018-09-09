var crypto = require('crypto');
var db = require('./db.js');

//Crea un hash sha256 a partir de una cadena de texto
module.exports.create_hash = function(text){
    var hash = crypto.createHash('sha256').update(text, 'utf-8').digest('hex')
    return hash;
};

//Función para crear el hash y validar la firma
module.exports.validate_transaction = function(json){
    var aux_sign = json.sign
    delete json.sign
    var serialized = JSON.stringify(json, null, 0);
    json.sign = aux_sign
    json.hash = module.exports.create_hash(serialized)
    return new Promise((suc, rej) => {
        db.getpk(json.transmitter)
        .then(function(pk){
            var verify = crypto.createVerify('SHA256');
            verify.update(serialized);
            correct = verify.verify(pk, json.sign, 'hex');
            if (correct)
                suc();
            else
                rej("Incorrect sign");
        }, function(msg){ rej(msg); });
    });
};