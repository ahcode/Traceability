var crypto = require('crypto');
var db = require('./db.js');

module.exports.create_hash = function(text){
    var hash = crypto.createHash('sha256').update(text, 'utf-8').digest('hex')
    return hash;
};

//Función para crear el hash y validar la firma
module.exports.validate_transaction = function(json){
    var aux_sign = json["sign"]
    delete json["sign"]
    var serialized = JSON.stringify(json, null, 0);
    json["sign"] = aux_sign
    json["hash"] = module.exports.create_hash(serialized, ['type', 'mode', 'transmitter', 'timestamp', 'data'])
    return new Promise((suc, rej) => {
        db.getpk(json["transmitter"])
        .then(function(pk){
            var verify = crypto.createVerify('SHA256');
            verify.update(serialized);
            correct = verify.verify(pk, json["sign"], 'hex');
            if (correct)
                suc();
            else
                rej("Bad Sign");
        }, function(msg){ rej(msg); });
    });
};