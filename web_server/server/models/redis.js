const fs = require("fs");
const path = require("path");
const yaml = require('js-yaml');
const redis = require('redis');
var service = {};

var config = {};
try {
    config = yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../../../config.yaml'), 'utf8'));
} catch (e) {
    console.log(e);
    throw e;
}

const client = redis.createClient(config.redis.port, config.redis.host);
const subscriber = redis.createClient(config.redis.port, config.redis.host);
const publisher = redis.createClient(config.redis.port, config.redis.host);

client.on('connect', () => {
    console.log('redis connected');
});

service.getRedis = () => {
    return client;
}

service.getPublisher = () => {
    return publisher;
}

service.getSubscriber = () => {
    return subscriber;
}

module.exports = service;


