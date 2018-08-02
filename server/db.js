const pg = require('pg');
const pool = new pg.Pool();

module.exports.newkey = function(name, hash, public_key){
    //active = TRUE por defecto solo para pruebas
    query = "INSERT INTO keys (name, hash, public_key, active) VALUES ('" + name + "', '" + hash + "', '" + public_key + "', TRUE);"
    
    return new Promise((suc, rej) => {
        pool.query(query, (err, res) => {
                if (err){
                    if (err.code == '23505')
                        rej("Duplicated key");
                    else{
                        console.log("DATABASE ERROR");
                        rej("Database error");
                    }
                }else
                    suc();
            }
        )
    })
}

module.exports.newtransaction = function(transaction){
    var query = "INSERT INTO transactions (hash, type, mode, transmitter, receiver, client_timestamp, transaction_data, sign) \
    VALUES ('" + transaction.hash + "', " + transaction.type + ", " + transaction.mode + ", '" + transaction.transmitter + "', ";
    if (transaction.receiver){
        query += "'" + transaction.receiver + "', ";
    }else{
        query += "NULL, ";
    }
    query += "to_timestamp(" + transaction.timestamp + "), '" + JSON.stringify(transaction.data, null, 0) + "', '" + transaction.sign + "');"
    
    return new Promise((suc, rej) => {
        pool.query(query, (err, res) => {
                if (err){
                    if (err.code != '23505') //Si la transacción está repetida, no hace nada
                        console.log("DATABASE ERROR");
                }else
                    suc();
            }
        )
    })
}

module.exports.getpk = function(key_hash){
    query = "SELECT public_key FROM keys WHERE hash = '" + key_hash + "' and active = true;"
    return new Promise((suc, rej) => {
        pool.query(query, (err, res) => {
            if (err){
                console.log("DATABASE ERROR");
                rej("Database error.")
            }else if (res.rowCount == 0)
                rej("The key doesn't exist")
            else
                suc(res.rows[0].public_key);
        });
    });
}

module.exports.new_available_inputs = function(key, product, inputs){
    return;
}

module.exports.del_available_inputs = function(key, product){
    return;
}

module.exports.get_available_inputs = function(key, product){
    return;
}

module.exports.update_available_inputs = function(key, product, inputs){
    return;
}