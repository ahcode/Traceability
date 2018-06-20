var config = require('./config.json')

module.exports.checkregisterformat = function(json){
    if (!json.hasOwnProperty("name") || typeof json["name"] != 'string' ||
        !json.hasOwnProperty("key") || typeof json["key"] != 'string')
        return false;
    else
        return true;
}

module.exports.checktransactionformat = function(json){
    var now = parseInt((new Date()).getTime() / 1000);
    //console.log(now);
    if (!json.hasOwnProperty("type") || typeof json["type"] != 'number' ||
        json["type"] < 0 || json["type"] > 2 ||
        !json.hasOwnProperty("mode") || typeof json["type"] != 'number' ||
        json["mode"] < 0 || json["mode"] > 3 ||
        !json.hasOwnProperty("transmitter") || typeof json["transmitter"] != 'string' ||
        !json.hasOwnProperty("timestamp") || typeof json["timestamp"] != 'number' ||
        json["timestamp"] > now + config.seconds_threshold || json["timestamp"] < now - config.max_seconds_delay ||
        !json.hasOwnProperty("data") || typeof json["data"] != 'object' ||
        !json.hasOwnProperty("sign") || typeof json["sign"] != 'string'
    )
        //TODO falta comprobar el interior de data
        return false;
    else
        return true;
}