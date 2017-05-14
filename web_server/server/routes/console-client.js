var express = require('express');
var router = express.Router();
const redis = require("../models/redis");
const redisClient = redis.getRedis();
const redisSubscriber = redis.getSubscriber();
const mongoose = require('mongoose');
const ServiceManager = mongoose.model('ServiceManager');
const ServiceChildInfo = mongoose.model('ServiceChildInfo');

const serviceManagersKey = "serviceManagers";


var service = {};

service.getAllManagers = (query) => {
    return new Promise((resolve, reject) => {
        ServiceManager.find(query).sort({ timestamp: -1 }).exec((err, all) => {
            if (err) {
                reject(err);
                return;
            }
            resolve(all);
        })
    })
};

service.getChildrenInfo = (query) => {
    return new Promise((resolve, reject) => {
        ServiceChildInfo.find(query).sort({ timestamp: -1 }).exec((err, all) => {
            if (err) {
                reject(err);
                return;
            }
            resolve(all);
        })
    })
};

var emitAllManager = (socket, query) => {
    service.getAllManagers(query).then((managers) => {
        socket.emit('managers', managers);
    }).catch(err => {
        console.error(err);
    })
};

var emitChildrenInfo = (socket, query) => {
    service.getChildrenInfo(query).then((info) => {
        socket.emit('childInfo', info);
    }).catch(err => {
        console.error(err);
    })
};

service.init = (io) => {
    io.on('connection', (socket) => {

        redisSubscriber.on("message", (channel, message) => {
            console.log(`${channel}: ${message}`);
            if (channel == "managers") {
                emitAllManager(socket, {});
            }
        });

        redisSubscriber.subscribe("managers");

        socket.on('get-managers', (query) => {
            emitAllManager(socket, query);
        });

        socket.on('get-manager', () => {
            emitAllManager(socket, query);
        });

        // parentId, childId
        socket.on('get-childInfo', (query) => {
            emitChildrenInfo(socket, query);
        })
    })
}

module.exports = service;