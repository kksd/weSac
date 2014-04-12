var Logger = require("../tools/logger.js");
var logger = new Logger();
function roomKeeper(){
	var roomList = {};
	var self = this;

	this.say = function(something){
		logger.log(something);
	}
	
}


module.exports = roomKeeper;

