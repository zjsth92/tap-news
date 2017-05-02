var services = {};

var jayson = require('jayson');
var config = require("../../../config.json")

var client = jayson.client.http({
    port: config.port,
    hostname: config.host
});

// Test RPC method
services.add = function add(a, b, callback) {
    client.request('add', [a, b], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

module.exports = services;
