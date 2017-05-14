const mongoose = require('mongoose');


const ChildSchema = new mongoose.Schema({
    pid: Number,
    name: String,
    filePath: String
});

const ServiceManagerSchema = new mongoose.Schema({
    socketId: String,
    timestamp: {
        type: Date,
        default: Date.now()
    },
    name: { type: String, required: true, unique: true },
    pid: { type: Number, required: true },
    host: String,
    platform: String,
    totalMemory: Object,
    state: {
        type: String,
        default: "running",
        enum: ['running', 'terminated']
    },
    children: [ChildSchema]
});

module.exports = mongoose.model('ServiceManager', ServiceManagerSchema);