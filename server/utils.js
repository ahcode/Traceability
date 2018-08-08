var config = require('./config.json')
var db = require('./db.js')

module.exports.checkregisterformat = function(json){
    if (!json.hasOwnProperty("name") || typeof json.name != 'string' ||
        !json.hasOwnProperty("key") || typeof json.key != 'string')
        return false;
    else
        return true;
};

module.exports.checktransactionformat = function(json){
    if (!json.hasOwnProperty("type") || typeof json.type != 'number' ||
        json.type < 0 || json.type > 2){
        return {'correct' : false, 'msg' : "type must be an integer between 0 and 2"}
    }
    if (!json.hasOwnProperty("mode") || typeof json.mode != 'number' ||
        json.mode < 0 || json.mode > 3){
        return {'correct' : false, 'msg' : "mode must be an integer between 0 and 3"}
    }
    if (!json.hasOwnProperty("transmitter") || typeof json.transmitter != 'string'){
        return {'correct' : false, 'msg' : "transmitter must be an string"}
    }
    if (!json.hasOwnProperty("timestamp") || typeof json.timestamp != 'number'){
        return {'correct' : false, 'msg' : "timstamp must be an integer"}
    }
    var now = parseInt((new Date()).getTime() / 1000);
    if (json.timestamp > now + config.seconds_threshold ||
        json.timestamp < now - config.max_seconds_delay){
        return {'correct' : false, 'msg' : "timestamp is different from the server time"}
    }
    if (!json.hasOwnProperty("data") || typeof json.data != 'object'){
        return {'correct' : false, 'msg' : "data must be a json serialized object"}
    }
    if (!json.hasOwnProperty("sign") || typeof json.sign != 'string'){
        return {'correct' : false, 'msg' : "sign must be a string"}
    }
    
    //TODO falta comprobar el interior de data
    
    return {'correct' : true};
};

//Actualiza la tabla available_inputs
module.exports.update_inputs = function(transaction){
    //Si no hay receptor, la transacción la recibe el transmisor
    if (transaction.hasOwnProperty('receiver'))
        var receiver = transaction.receiver;
    else
        var receiver = transaction.transmitter;
    
    //Establecer productos de entrada y salida de la transacción
    var p_in, p_out;
    var same_out = false;
    if (transaction.mode == 3 && transaction.type != 0){
        return; //TODO
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
    for (let i = 0; i < p_in.length; i++){
        process_input(transaction.transmitter, transaction.hash, transaction.mode, p_in[i][0], p_in[i][1])
        .then(function(quantity){
            if (same_out && p_out[i][1] == null)
                process_output(receiver, transaction.hash, p_out[i][0], quantity);
        });
    }

    //Añadir productos al receptor
    var new_id = null;
    for(let i = 0; i < p_out.length; i++){
        if (p_out[i][1] != null){
            if (transaction.data.hasOwnProperty('new_id'))
                new_id = transaction.data.new_id;
            else
                new_id = null;
            process_output(receiver, transaction.hash, p_out[i][0], p_out[i][1], new_id);
        }
    };
};

function process_input(key, transaction_hash, mode, product, quantity){
    return db.get_available_inputs(key, product)
    .then(function(inputs){
        var q_out = null;
        if(inputs == null){
            //TODO
            //No existe la entrada, se está utilizando producto que no posee
            //Marcar transacción erronea
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
                    //TODO
                    //Está gastando más producto del que posee
                    //Marcar transacción erronea
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

function process_output(key, transaction_hash, product, quantity, new_id){
    db.get_available_inputs(key, product)
    .then(function(inputs){
        new_input = {'t_hash': [transaction_hash], 'quantity': quantity};
        if (new_id){
            new_input.id = new_id;
            //TODO
            //Registrar nuevo id en tabla de bd
        }
        if(!inputs){
            inputs = [new_input];
            db.new_available_inputs(key, product, inputs);
        }else{
            inputs.push(new_input);
            db.update_available_inputs(key, product, inputs);
        }
    });
}

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