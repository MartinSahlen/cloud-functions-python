exports.serve = function(req, res) {
    res.end('Hello world!')
}

exports.serveApi = require('./api');
