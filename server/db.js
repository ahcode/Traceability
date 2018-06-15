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