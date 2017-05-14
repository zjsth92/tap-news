const spawn = require('child_process').spawn;
var fs = require('fs');
var service = {};


service.run = function (path, name) {
    let pyShell = spawn("python", ["-u", path]);
    console.log(`${name} is running on pid: ${pyShell.pid}`);
    var logSteam = fs.createWriteStream(`${__dirname}/${name}.log`, {flags : 'a'});
    logSteam.write(`\n================ time ${new Date()} ===========================\n`);
    logSteam.write(`================ running on pid ${pyShell.pid} ================\n`);

    // Handle normal output
    // pyShell.stdout.on('data', (data) => {
    //     console.log(data.toString('utf8'));
    // });
    pyShell.stdout.pipe(logSteam);

    // Handle error output
    pyShell.stderr.pipe(logSteam);

    let exitHandler = (code) => {
        console.log(`Process:${pyShell.pid},Name:${name} quit with code:${code}`);
        // heartbeat.unregister(pyShell.pid);
    }

    pyShell.on('SIGINT', exitHandler);

    pyShell.on('uncaughtException', exitHandler);

    pyShell.on('exit', exitHandler);

    return pyShell.pid
}

module.exports = service;
