var db = require('./db.js')
var fs = require('fs');
var config_filename = './config.json'
var config = require(config_filename)

//Comprueba que el formato de la petición de registro sea correcto
module.exports.checkregisterformat = function(json){
    if (!json.hasOwnProperty("name") || typeof json.name != 'string' ||
        !json.hasOwnProperty("key") || typeof json.key != 'string')
        return {'error' : "json format is not correct"};
    return {};
};

//Comprueba que el formato de la transacción sea correcto
module.exports.checktransactionformat = function(json){
    if (!json.hasOwnProperty("type") || typeof json.type != 'number' ||
        json.type < 0 || json.type > 2){
        return {'error' : "type must be an integer between 0 and 2"}
    }
    if (!json.hasOwnProperty("mode") || typeof json.mode != 'number' ||
        json.mode < 0 || json.mode > 3){
        return {'error' : "mode must be an integer between 0 and 3"}
    }
    if (!json.hasOwnProperty("transmitter") || typeof json.transmitter != 'string'){
        return {'error' : "transmitter must be an string"}
    }
    if (!json.hasOwnProperty("timestamp") || typeof json.timestamp != 'string'){
        return {'error' : "timstamp must be an integer"}
    }
    var now = parseInt((new Date()).getTime() / 1000);
    var timestamp = parseFloat(json.timestamp);
    if (timestamp > now + config.seconds_threshold ||
        timestamp < now - config.max_seconds_delay){
        return {'error' : "timestamp is different from the server time"}
    }
    if (!json.hasOwnProperty("data") || typeof json.data != 'object'){
        return {'error' : "data must be a json serialized object"}
    }
    if (!json.hasOwnProperty("sign") || typeof json.sign != 'string'){
        return {'error' : "sign must be a string"}
    }
    
    return {};
};

//Actualiza la tabla available_inputs, enlaca transacciones y registra identificadores de productos
module.exports.update_inputs = function(transaction){
    //Si no hay receptor, la transacción la recibe el transmisor
    if (transaction.hasOwnProperty('receiver'))
        var receiver = transaction.receiver;
    else
        var receiver = transaction.transmitter;
    
    //Establecer productos de entrada y salida de la transacción
    var p_in, p_out;
    var same_out = false;
    var process_in = true;
    var process_out = true;
    if (transaction.mode == 3 && transaction.type != 0){ //Transacciones con ID
        process_in = false; process_out = false;
        if (transaction.type == 1){
            p = transaction.data.product[0];
            db.update_product_id(p[1], transaction.transmitter, transaction.hash, p[0], null, transaction.data.destination)
        }else{
            if (transaction.data.hasOwnProperty('product')){
                p = transaction.data.product[0];
                db.update_product_id(p[1], transaction.transmitter, transaction.hash, p[0], receiver)
            }else{
                p_in = transaction.data.product_in;
                p_out = transaction.data.product_out;
                db.update_product_id(p_in[1], transaction.transmitter, transaction.hash, p_in[0])
                process_out = true;
            }
        }
    }else{
        if (transaction.type == 0){
            p_out = transaction.data.product;
            p_in = [];
        }else if (transaction.type == 1){
            p_in = transaction.data.product;
            p_out = [];
        }else{ //type 2
            if (transaction.data.hasOwnProperty('product')){
                p_in = transaction.data.product;
                p_out = transaction.data.product;
                same_out = true;
            }else{
                p_in = transaction.data.product_in;
                p_out = transaction.data.product_out;
            }
        }
    }
    //Eliminar productos utilizados del emisor y localizar transacciones precedentes
    if (process_in){
        for (let i = 0; i < p_in.length; i++){
            process_input(transaction.transmitter, transaction.hash, transaction.mode, p_in[i][0], p_in[i][1])
            .then(function(quantity){
                if (same_out && p_out[i][1] == null)
                    process_output(receiver, transaction.hash, p_out[i][0], quantity);
            });
        }
    }

    //Añadir productos al receptor
    if (process_out){
        if (!transaction.data.hasOwnProperty('new_id')){
            for(let i = 0; i < p_out.length; i++){
                if (p_out[i][1] != null){
                    process_output(receiver, transaction.hash, p_out[i][0], p_out[i][1]);
                }
            };
        }else{
            db.new_id(transaction.data.new_id, receiver, transaction.hash, p_out[0][0])
        }
    }
};

//Procesa los productos de entrada
function process_input(key, transaction_hash, mode, product, quantity){
    return db.get_available_inputs(key, product)
    .then(function(inputs){
        var q_out = null;
        if(inputs == null){
            //No existe la entrada, se está utilizando producto que no posee
            //Marcar transacción erronea
            db.set_error(transaction_hash, product);
        }else{
            if(mode == 0)
                mix_product(inputs);
            if(quantity != null){
                while(quantity > 0 && inputs.length > 0){
                    if (mode == 2) //stack
                        el = inputs.length - 1;
                    else
                        el = 0;
                    db.set_inputs(transaction_hash, inputs[el].t_hash, product)
                    if (quantity < inputs[el].quantity){
                        inputs[el].quantity -= quantity;
                        quantity = 0;
                    }else{
                        quantity -= inputs[el].quantity;
                        inputs.splice(el, 1);
                    }
                }
                if(quantity > 0){
                    //Está gastando más producto del que posee
                    //Marcar transacción erronea
                    db.set_error(transaction_hash, product);
                }
            }else{
                if (mode == 2) //stack
                    el = inputs.length - 1;
                else
                    el = 0;
                q_out = inputs[el].quantity;
                db.set_inputs(transaction_hash, inputs[el].t_hash, product)
                db.set_quantity(transaction_hash, product, q_out)
                inputs.splice(el, 1);
            }
            if (inputs.length > 0)
                db.update_available_inputs(key, product, inputs);
            else
                db.del_available_inputs(key, product);
        }
        return q_out;
    });
}

//Procesa los productos de salida
function process_output(key, transaction_hash, product, quantity){
    db.get_available_inputs(key, product)
    .then(function(inputs){
        new_input = {'t_hash': [transaction_hash], 'quantity': quantity};
        if(!inputs){
            inputs = [new_input];
            db.new_available_inputs(key, product, inputs);
        }else{
            inputs.push(new_input);
            db.update_available_inputs(key, product, inputs);
        }
    });
}

//Mezcla los productos que posee una clave para combinar los orígenes
function mix_product(inputs){
    if(inputs.length > 1){
        var sum = 0;
        var transactions_array = [];
        for(i = 0; i < inputs.length; i++){
            sum += inputs[i].quantity;
            transactions_array.push(...inputs[i].t_hash);
        }
        inputs.splice(0, inputs.length);
        inputs.push({'t_hash': transactions_array, 'quantity': sum});
    }
}

//Establece el valor de una variable de configuración
module.exports.set_config_variable = function(name, value){
    config[name] = value;
    fs.writeFile(config_filename, JSON.stringify(config, null, 4), (err) => {
        if (err) console.log(err);
    });
}

//Devuelve el valor de una variable de configuración
module.exports.get_config_variable = function(name){
    if(config.hasOwnProperty(name)){
        return config[name];
    }else{
        throw 'DoesNotExist'
    }
}