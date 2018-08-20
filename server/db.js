const pg = require('pg');
const pool = new pg.Pool();

module.exports.newkey = function(name, hash, public_key){
    query = "INSERT INTO keys (name, hash, public_key) VALUES ($1, $2, $3);"
    values = [name, hash, public_key]
    return new Promise((suc, rej) => {
        pool.query(query, values, (err, res) => {
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
        );
    });
}

module.exports.newtransaction = function(transaction){
    var query = "INSERT INTO transactions (hash, type, mode, transmitter, receiver, client_timestamp, raw_client_timestamp, transaction_data, sign) \
    VALUES ($1, $2, $3, $4, $5, to_timestamp($6), '" + transaction.timestamp + "', $7, $8)";
    values = [transaction.hash, transaction.type, transaction.mode, transaction.transmitter, transaction.receiver? transaction.receiver : null, transaction.timestamp, transaction.data, transaction.sign];
    return new Promise((suc, rej) => {
        pool.query(query, values, (err, res) => {
                if (err){
                    if (err.code != '23505') //Si la transacción está repetida, no hace nada
                        console.log("DATABASE ERROR");
                }else
                    suc();
            }
        );
    });
}

module.exports.getpk = function(key_hash){
    query = "SELECT public_key FROM keys WHERE hash = $1 AND current_status = 'active';"
    return new Promise((suc, rej) => {
        pool.query(query, [key_hash], (err, res) => {
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
    query = "INSERT INTO available_inputs (key_hash, product, inputs) VALUES ($1, $2, $3)";
    values = [key, product, inputs];
    pool.query(query, values, (err, res) => {
            if (err){
                console.log("DATABASE ERROR");
            }
        }
    );
}

module.exports.del_available_inputs = function(key, product){
    query = "DELETE FROM available_inputs WHERE key_hash = $1 AND product = $2";
    pool.query(query, values, (err, res) => {
            if (err){
                console.log("DATABASE ERROR");
            }
        }
    );
}

module.exports.get_available_inputs = function(key, product){
    query = "SELECT inputs FROM available_inputs WHERE key_hash = $1 AND product = $2";
    values = [key, product];
    return new Promise((suc, rej) => {
        pool.query(query, values, (err, res) => {
            if (err)
                console.log("DATABASE ERROR");
            else if (res.rowCount == 0)
                suc(null);
            else
                suc(res.rows[0].inputs);
        });
    });
}

module.exports.update_available_inputs = function(key, product, inputs){
    query = "UPDATE available_inputs SET inputs = $1 WHERE key_hash = $2 AND product = $3";
    values = [inputs, key, product]
    pool.query(query, values, (err, res) => {
            if (err){
                console.log("DATABASE ERROR");
            }
        }
    );
}

module.exports.set_inputs = function(transaction, input_list, product){
    query = "INSERT INTO t_inputs VALUES ($1, $2, $3);";
    values = [transaction, null, product];
    for(i = 0; i < input_list.length; i++){
        values[1] = input_list[i];
        pool.query(query, values, (err, res) => {
            if (err){
                console.log("DATABASE ERROR");
            }
        });
    }
}

module.exports.set_quantity = function(transaction, product, quantity){
    var obj = {};
    obj[product] = quantity;
    query = "UPDATE transactions SET updated_quantity = CASE WHEN updated_quantity IS NULL THEN $1 ELSE updated_quantity::jsonb || $1 END WHERE hash = $2 ;";
    pool.query(query, [obj, transaction], (err, res) => {
        if (err){
            console.log("DATABASE ERROR");
        }
    });
}

module.exports.update_product_id = function(id, key, transaction_hash, product, new_owner=null, destination=null){
    query = "SELECT last_transaction FROM product_id WHERE id = $1 AND product = $2 AND owner = $3";
    values = [id, product, key];
    pool.query(query, values, (err, res) => {
        if (err){
            console.log("DATABASE ERROR");
        }else{
            query = "UPDATE product_id SET last_transaction = $1, owner = $2, destination = $3 WHERE id = $4 AND product = $5 AND owner = $6";
            values = [transaction_hash, new_owner, destination, id, product, key];
            if(res.rowCount == 1){
                pool.query(query, values, (err, res) => {
                    if (err){
                        console.log("DATABASE ERROR");
                    }
                });
                module.exports.set_inputs(transaction_hash, [res.rows[0].last_transaction], product);
            }
        }
    });
    
}

module.exports.new_id = function(id, key, transaction_hash, product){
    query = "INSERT INTO product_id (id, product, owner, first_transaction, last_transaction) VALUES ($1, $2, $3, $4, $4)";
    values = [id, product, key, transaction_hash]
    pool.query(query, values, (err, res) => {
        if (err){
            console.log("DATABASE ERROR");
        }
    });
}

module.exports.check_key = function(keyhash){
    query = "SELECT FROM keys WHERE current_status='active' AND hash=$1";
    return new Promise((suc, rej) => {
        pool.query(query, [keyhash], (err, res) => {
                if (err){
                    console.log("DATABASE ERROR");
                }else if(res.rowCount == 0){
                    rej();
                }else{
                    suc();
                }
            }
        );
    });
}