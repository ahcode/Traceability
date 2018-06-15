var crypto = require('crypto');

module.exports.create_hash = function(text){
    var hash = crypto.createHash('sha256').update(text, 'ascii').digest('hex')
    return hash;
}