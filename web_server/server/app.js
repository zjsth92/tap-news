var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
var passport = require('passport');
var cors = require('cors');

var index = require('./routes/index');
var news = require('./routes/news');
var auth = require('./routes/auth');

var config = require('../../config.json');
require('./models/index.js').connect(`mongodb://${config.mongodb.host}:${config.mongodb.port}/${config.mongodb.news_table}`);

var app = express();

// view engine setup
app.set('views', path.join(__dirname, './views/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

// TODO: remove this after development is done
app.use(cors());
app.use(bodyParser.json());

app.use('/', index);
app.use('/news', news);

// load passport strategies
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup');
var localLoginStrategy = require('./passport/login');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// pass the authenticaion checker middleware
const authMiddleware = require('./middleware/auth');
app.use('/news', authMiddleware);

app.use('/', index);
app.use('/news', news);
app.use('/auth', auth);


// catch 404 and forward to error handler
app.use(function (req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  res.render('error', { "error": err, "message": "Page Not Found" });
});

module.exports = app;
