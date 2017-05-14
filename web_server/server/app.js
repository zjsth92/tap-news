var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
var passport = require('passport');
var cors = require('cors');
var yaml = require('js-yaml');
var fs = require('fs');

var config = {};
try {
  config = yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../../config.yaml'), 'utf8'));
} catch (e) {
  console.log(e);
}
var mongodb_user = "cs503"
var mongodb_pwd = "cs503_tap_news"
var mongodb_url = `mongodb://${mongodb_user}:${mongodb_pwd}@${config.mongodb.host}:${config.mongodb.port}/${config.mongodb.db_name}`
require('./models/index.js').connect(mongodb_url);

var port = normalizePort(process.env.PORT || '4000');

var app = express();
var server = require('http').Server(app);
app.set('port', port);
var io = require('socket.io')(server);

// view engine setup
// app.set('views', path.join(__dirname, './views/'));
// app.set('view engine', 'jade');
// app.use('/static', express.static(path.join(__dirname, '../build/static/')));

// TODO: remove this after development is done
app.use(cors());
app.use(bodyParser.json());

// load routers
var newsRouter = require('./routes/news');
var authRouter = require('./routes/auth');
var consoleManagerRouter = require('./routes/console-manager').init(io.of('/console/manager'));
var consoleClientRouter = require('./routes/console-client').init(io.of('/console/client'));

// load passport strategies
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup');
var localLoginStrategy = require('./passport/login');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// pass the authenticaion checker middleware
const authMiddleware = require('./middleware/auth');
app.use('/news', authMiddleware);

app.use('/news', newsRouter);
app.use('/auth', authRouter);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  res.sendFile("index.html", { root: path.join(__dirname, '../build/') });
});

server.listen(port, (err)=>{
  if(err) console.error(err);
  console.log(`Server is running on port: ${port}`)
});

/**
 * Normalize a port into a number, string, or false.
 */
function normalizePort(val) {
  var port = parseInt(val, 10);

  if (isNaN(port)) {
    // named pipe
    return val;
  }

  if (port >= 0) {
    // port number
    return port;
  }

  return false;
}


module.exports = app;
