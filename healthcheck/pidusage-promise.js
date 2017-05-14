var pusage = require('pidusage')
var service = {};


service.getPusage = (pid, name) => {
    return new Promise(function (resolve, reject) {
        var usage = {
            "pid": pid,
            "pcpu": null,
            "pmemory": {
                "size": null,
                "unit": null
            },
            "name": name
        }
        pusage.stat(pid, (err, stat) => {
            if (err) {
                reject(err);
                return;
            }

            if (!stat) { 
                resolve(stat) 
                return;
            };
            usage.pcpu = stat.cpu
            usage.pmemory = {
                "size": (stat.memory / (1024 * 1024)).toFixed(2),
                "unit": "MB"
            }
            resolve(usage);
        })
    });
};

service.getChildrenInfo = (runningChildren) => {
    return new Promise((resolve, reject) => {
        var childPromises = [];
        runningChildren.forEach((child) => {
            childPromises.push(service.getPusage(child.pid, child.name))
        })
        if (childPromises.length > 0) {
            Promise.all(childPromises).then((childrenInfo) => {
                console.log(childrenInfo);
                resolve(childrenInfo)
            }).catch(err => {
                reject(err);
            });
        } else {
            resolve([]);
        }

    })
};

module.exports = service;