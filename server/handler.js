var router = require('express').Router();

router.get('/new_transaction', function(req, res) {
   res.send("Get received.");
});

router.post('/new_transaction', function(req, res) {
    res.send("Post received.");
});

module.exports.router = router;