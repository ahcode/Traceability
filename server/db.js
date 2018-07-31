const pg = require('pg');
const pool = new pg.Pool();

module.exports.newkey = function(name, hash, public_key, callback){
    //active = TRUE por defecto solo para pruebas
    query = "INSERT INTO keys (name, hash, public_key, active) VALUES ('" + name + "', '" + hash + "', '" + public_key + "', TRUE);"
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

module.exports.newtransaction = function(transaction){
    var query = "INSERT INTO transactions (hash, type, mode, transmitter, receiver, client_timestamp, transaction_data, sign) \
    VALUES ('" + transaction["hash"] + "', " + transaction["type"] + ", " + transaction["mode"] + ", '" + transaction["transmitter"] + "', ";
    if (transaction["receiver"]){
        query += "'" + transaction["receiver"] + "', ";
    }else{
        query += "NULL, ";
    }
    query += "to_timestamp(" + transaction["timestamp"] + "), '" + transaction["data"] + "', '" + transaction["sign"] + "');"
    pool.query(
        query,
        (err, res) => {
            //TODO mejorar tratamiento de errores
            if (err)
                console.log("DATABASE ERROR");
        }
    )
}

module.exports.getpk = function(key_hash, callback){
    query = "SELECT public_key FROM keys WHERE hash = '" + key_hash + "' and active = true;"
    pool.query(
        query,
        (err, res) => {
            //TODO mejorar tratamiento de errores
            if (err){
                console.log("DATABASE ERROR");
                callback(true);
            }else if (res.rowCount == 0)
                callback(true);
            else
                callback(false, res.rows[0].public_key);
        }
    )
}