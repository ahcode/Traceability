var config = require('./config.json')

module.exports.checkregisterformat = function(json){
    if (!json.hasOwnProperty("name") || typeof json["name"] != 'string' ||
        !json.hasOwnProperty("key") || typeof json["key"] != 'string')
        return false;
    else
        return true;
}

module.exports.checktransactionformat = function(json){
    if (!json.hasOwnProperty("type") || typeof json["type"] != 'number' ||
        json["type"] < 0 || json["type"] > 2){
        return {'correct' : false, 'msg' : "type must be an integer between 0 and 2"}
    }
    if (!json.hasOwnProperty("mode") || typeof json["mode"] != 'number' ||
        json["mode"] < 0 || json["mode"] > 3){
        return {'correct' : false, 'msg' : "mode must be an integer between 0 and 3"}
    }
    if (!json.hasOwnProperty("transmitter") || typeof json["transmitter"] != 'string'){
        return {'correct' : false, 'msg' : "transmitter must be an string"}
    }
    if (!json.hasOwnProperty("timestamp") || typeof json["timestamp"] != 'number'){
        return {'correct' : false, 'msg' : "timstamp must be an integer"}
    }
    var now = parseInt((new Date()).getTime() / 1000);
    if (json["timestamp"] > now + config.seconds_threshold ||
        json["timestamp"] < now - config.max_seconds_delay){
        return {'correct' : false, 'msg' : "timestamp is different from the server time"}
    }
    if (!json.hasOwnProperty("data") || typeof json["data"] != 'object'){
        return {'correct' : false, 'msg' : "data must be a json serialized object"}
    }
    if (!json.hasOwnProperty("sign") || typeof json["sign"] != 'string'){
        return {'correct' : false, 'msg' : "sign must be a string"}
    }
    
    //TODO falta comprobar el interior de data
    
    return {'correct' : true};
}