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

// Get news summaries for a user
services.getNewsSummariesForUser = function getNewsSummariesForUser(user_id, page_num, callback) {
    client.request('getNewsSummariesForUser', [user_id, page_num], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Log a news click event for a user
services.logNewsClickForUser = function logNewsClickForUser(user_id, news_id) {
    client.request('logNewsClickForUser', [user_id, news_id], function(err, error, response) {
        if (err) throw err;
        console.log(response);
    });
}

module.exports = services;
