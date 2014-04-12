var express = require("express");
var initializer = require("./init/initializer");
var path = require('path');
var app = express();
var RoomKeeper = require("./core/roomKeeper.js");
var roomKeeper = new RoomKeeper();
var Logger = require("./tools/logger.js");
var logger = new Logger();
var config = require('./config.js');


app.set('port', process.env.PORT || 8000);
app.set('roomKeeper', roomKeeper);
app.set('views', __dirname + '/views'); // view folder
app.set('view engine', "jade"); // what template we use
app.engine('jade', require('jade').__express); // use template we specified
app.use(express.static(path.join(__dirname, 'apps'))); // specify the external javascript file


initializer.initialize(app, function (err) {
    if (err) {
        logger.log('Initialization failed.');
    }
    else {
        logger.log('Initialization completed.');
        var listener=app.listen(app.get('port'));
        logger.log("App is listening on port " + app.get('port'));
        var io = require('socket.io').listen(listener);
        io.set('log level', config.logging.level)
        logger.log("Socket is listenning on port " + app.get('port'));
    }
});
 
