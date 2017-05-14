const redis = require("../models/redis");
const redisClient = redis.getRedis();
const redisPublisher = redis.getPublisher();
const mongoose = require('mongoose');
const ServiceManager = mongoose.model('ServiceManager');
const ServiceChildInfo = mongoose.model('ServiceChildInfo');

const serviceManagersKey = "serviceManagers";

var service = {};

var registManager = (manager) => {
    manager.state = "running";
    ServiceManager.update({ name: manager.name }, manager, { upsert: true, sparse: true }, (err, data) => {
        if (err) {
            console.error(err); return;
        }
        console.log(data);
        redisClient.set(`${serviceManagersKey}:${manager.pid}`, JSON.stringify(manager));
        redisPublisher.publish("managers", `${manager.name} is now running`);
    })
}

var unregistManager = (socketId) => {
    ServiceManager.findOneAndUpdate({ socketId: socketId }, { state: "terminated" }, (err, manager) => {
        if (err) console.error(err)
        console.log(manager);
        if (manager) {
            redisClient.set(`${serviceManagersKey}:${manager.pid}`, JSON.stringify(manager));
            redisPublisher.publish("managers", `${manager.name} terminated`);
        }
    })
}

var receiveChildInfo = (childInfo) => {
    var newServiceChildInfo = new ServiceChildInfo(childInfo);
    newServiceChildInfo.save((err) => {
        if (err) {
            console.error(err); return;
        }
    })
};


service.init = (io) => {
    io.on('connection', (socket) => {
        socket.on('disconnect', (data) => {
            console.log(`disconnected ${data}`)
            unregistManager(socket.id);
        });

        socket.on('managers', (manager) => {
            manager.socketId = socket.id;
            manager.host = socket.handshake.headers.host;
            registManager(manager);
        });

        socket.on('child', (childInfo) => {
            receiveChildInfo(childInfo);
        })

    })
}





module.exports = service;