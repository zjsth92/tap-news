var os = require("os");
var systemInfo = require("./system-info")
var pusage = require('./pidusage-promise')

var service = {};

service.register = (name, pid, runningChildren, socket) => {
    socket.emit('managers', {
        "name": name,
        "pid": pid,
        "platform": systemInfo.getPlatform(),
        "totalMemory": {
            "size": systemInfo.getTotalMemo('gb'),
            "unit": "GB"
        },
        "children": runningChildren
    })
};

service.sendChildrenInfo = (runningChildren, socket) => {
    pusage.getChildrenInfo(runningChildren).then((info) => {
        if (Array.isArray(info)) {
            info.forEach((childInfo) => {
                socket.emit('child', childInfo);
            });
        } else {
            socket.emit('child', info);
        }

    }).catch(err => console.error)
};

module.exports = service;