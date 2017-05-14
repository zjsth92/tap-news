var path = require('path')
var fs = require('fs');
var yaml = require('js-yaml');

// var heartbeat = require('./heartbeat')
var socketManager = require('./socket-manager');
var excuter = require('./py-excuter');

var runningChildren = [];
var isRegisted = false;

console.log(`main process: ${process.pid}`)

var runConfig = {};
var name = null;
var socket = null;
let runFilePath = process.argv[2];
try {
    runConfig = yaml.safeLoad(fs.readFileSync(path.join(__dirname, runFilePath), 'utf8'));
    socket = require('socket.io-client')(`${runConfig.endpoint}/console/manager`);
    name = runConfig.name
    let pyList = runConfig.python;
    pyList.forEach(runPyFile);

    socket.on('connect', function () {
        console.log("connected");
        if (!isRegisted) {
            socketManager.register(name, process.pid, runningChildren, socket);
            isRegisted = true;
        }
    });

    socket.on('disconnect', function () {
        console.log("disconnected")
    });

    socket.on('send-log', function (child) {
        console.log(child);
    });


    process.on("exit", exitHandler)

    //catches ctrl+c event
    process.on('SIGINT', exitHandler);

    //catches uncaught exceptions
    process.on('uncaughtException', exitHandler);

    // schedule heartbeat
    var heartbeatJobId = setInterval(function () {
        runningChildren.forEach((child) => {
            try {
                process.kill(child.pid, 0);
            } catch (err) {
                console.log(`${child.name} is stoped on pid: ${child.pid}`)
                let index = runningChildren.indexOf(child);
                if (index != -1) {
                    runningChildren.splice(index, 1);
                }
            }
        });
        // socketManager.sendChildrenInfo(runningChildren, socket);
    }, 1000 * 3) //3s

} catch (e) {
    console.error(e);
    process.exit();
}




function exitHandler(data) {
    if (data) console.error(data);
    console.log(`main process exit: clean child processes: ${runningChildren}`);
    let len = runningChildren.length;
    for (var i = 0; i < len; i++) {
        var pid = runningChildren.pop().pid;
        console.log(`Kill process: ${pid}`);
        process.kill(pid);
    }
    process.exit();
}

function runPyFile(pyFile) {
    let pid = excuter.run(pyFile.path, pyFile.name);
    runningChildren.push({ pid: pid, name: pyFile.name, filePath: pyFile.path });
}
