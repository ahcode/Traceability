var crypto = require('crypto');

module.exports.create_hash = function(text){
    var hash = crypto.createHash('sha256').update(text, 'ascii').digest('hex')
    return hash;
};

module.exports.validate_transaction = function(json){
    //Función para crear el hash y validar la firma
    //MANTENER EL ORDEN PARA CREAR EL HASH
    return true;
};