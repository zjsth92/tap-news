const mongoose = require('mongoose');

const ServiceChildInfoSchema = new mongoose.Schema({
    parentPid: Number,
    childPid: Number,
    name: String,
    time: {
        type: Date,
        default: Date.now()
    },
    pcpu: Number,
    pmemory: Object,
});

module.exports = mongoose.model('ServiceChildInfo', ServiceChildInfoSchema);