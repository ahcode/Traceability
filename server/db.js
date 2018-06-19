const pg = require('pg');
const pool = new pg.Pool();

module.exports.newkey = function(name, hash, public_key, callback){
    //active = TRUE por defecto solo para pruebas
    pool.query(
        "INSERT INTO keys (name, hash, public_key, active) \
        VALUES ('" + name + "', '" + hash + "', '" + public_key + "', TRUE);",
        (err, res) => {
            //TODO mejorar tratamiento de errores
            if (err)
                callback(true);
            else
                callback(false);
        }
    )
}

module.exports.newtransaction = function(hash, type, transmitter, receiver, client_timestamp, data, sign, callback){
    var query = "INSERT INTO transactions (hash, type, transmitter, receiver, client_timestamp, transaction_data, sign) \
    VALUES ('" + hash + "', " + type + ", '" + transmitter + "', ";
    if (receiver){
        query += "'" + receiver + "', ";
    }else{
        query += "NULL, ";
    }
    query += "to_timestamp(" + client_timestamp + "), '" + data + "', '" + sign + "');"
    pool.query(
        query,
        (err, res) => {
            //TODO mejorar tratamiento de errores
            if (err)
                callback(true);
            else
                callback(false);
        }
    )
}