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
    var p_in, p_out, q_in, q_out;
    if (transaction.mode == 3 && transaction.type != 0){
        return; //TODO
    }else{
        if (transaction.type == 0){
            p_out = [transaction.data.product];
            q_out = [transaction.data.quantity];
            p_in = []; q_in = [];
        }else if (transaction.type == 1){
            p_in = [transaction.data.product];
            if (transaction.data.hasOwnProperty('quantity'))
                q_in = [transaction.data.quantity];
            else
                q_in = null;
            p_out = []; q_out = [];
        }else{ //type 2
            if (typeof transaction.data.product == 'string'){
                p_out = [transaction.data.product];
                if (transaction.data.hasOwnProperty('quantity')){
                    q_out = [transaction.data.quantity];
                }else{
                    q_out = null;
                }
            }else{
                p_out = transaction.data.product;
                if (transaction.data.hasOwnProperty('quantity')){
                    q_out = transaction.data.quantity;
                }else{
                    q_out = null;
                }
            }
            if (transaction.data.hasOwnProperty('product_in')){
                if (typeof transaction.data.product_in == 'string'){
                    p_in = [transaction.data.product_in];
                    if (transaction.data.hasOwnProperty('quantity_in'))
                        q_in = [transaction.data.quantity_in];
                    else
                        q_in = null;
                }else{
                    p_in = transaction.data.product_in;
                    if (transaction.data.hasOwnProperty('quantity_in'))
                        q_in = transaction.data.quantity_in;
                    else
                        q_in = null;
                }
            }else{
                p_in = p_out;
                q_in = q_out;
            }
        }
    }

    //Eliminar productos utilizados del emisor y localizar transacciones precedentes
    used_inputs = [];
    for (i = 0; i < p_in.length; i++){
        db.get_available_inputs(transaction.transmitter, p_in[i])
        .then(function(inputs){
            if(inputs == null){
                //TODO
                //No existe la entrada, se está utilizando producto que no posee
                //Marcar transacción erronea
            }else{
                used = {'product': p_in[i], 'inputs': []}
                if(transaction.mode == 0)
                    mix_product(inputs);
                if(q_in){
                    while(q_in[i] > 0 && inputs.length > 0){
                        if (transaction.mode == 2) //stack
                            el = inputs.length - 1;
                        else
                            el = 0;
                        used.inputs.concat(inputs[el].t_hash);
                        if (q_in[i] < inputs[el].quantity){
                            inputs[el].quantity -= q_in[i];
                            q_in[i] = 0;
                        }else{
                            q_in[i] -= inputs[el].quantity;
                            inputs.splice(el, 1);
                        }
                    }
                    if(q_in > 0){
                        //TODO
                        //Está gastando más producto del que posee
                        //Marcar transacción erronea
                    }
                }else{
                    if (transaction.mode == 2) //stack
                        el = inputs.length - 1;
                    else
                        el = 0;
                    if (!q_out)
                        q_out = [inputs[el].quantity];
                    used.inputs.concat(inputs[el].t_hash);
                    inputs.splice(el, 1);
                }
                if (inputs.length > 0)
                    db.update_available_inputs(transaction.transmitter, p_in[i], inputs);
                else
                    db.del_available_inputs(transaction.transmitter, p_in[i]);
            }
        })
    }

    //Añadir productos al receptor
    for(i = 0; i < p_out.length; i++){
        db.get_available_inputs(receiver, p_out[i])
        .then(function(inputs){
            new_input = {'t_hash': [transaction.hash], 'quantity': q_out[i]};
            if (transaction.data.hasOwnProperty('new_id')){
                new_input.id == transaction.data.new_id;
                //TODO
                //Registrar nuevo id en tabla de bd
            }
            if(inputs == null){
                inputs = [new_input];
                db.new_available_inputs(transaction.transmitter, p_out[i], inputs);
            }else{
                inputs.push(new_input);
                db.update_available_inputs(transaction.transmitter, p_out[i], inputs);
            }
        });
    }
};

function mix_product(inputs){
    if(inputs.length > 1){
        var sum = 0;
        var transactions_array = [];
        for(i = 0; i < len(inputs); i++){
            sum += inputs[i].quantity;
            transactions_array.concat(inputs[i].t_hash);
        }
        inputs = {'t_hash': transactions_array, 'quantity': sum};
    }
}