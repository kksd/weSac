var config = require("../config.js");
function logger(){

    var LEVEL = {
        LOG: 1,
        INFO: 2,
        DEBUG: 3,
        WARNING: 4,
        ERROR: 5,
        CRITICAL: 6
    }

    var loggingLevel = config.logging.level;

    this.setLogging = function(level){
        loggingLevel = log
    }

    var reformat = function(tag, message){
        var ret = "  [" + tag + "] - " + message;
        return ret;
    }

    this.log = function(message){
        console.log(reformat('normal', message));
      };

    this.info = function(message){
        if(loggingLevel >= 2){
            console.log(reformat('info', message));
        }
    }

    this.debug = function(message){
        if(loggingLevel >= 3){
            console.log(reformat('debug', message));
        }
    }

    this.warning = function(message){
        if(loggingLevel >= 4){
            console.log(reformat('warning', message));
        }
    }

    this.ERROR = function(message){
        if(loggingLevel >= 5){
            console.log(reformat('ERROR', message));
        }
    }

    this.critical = function(message){
        if(loggingLevel >= 6){
            console.log(message);
        }
    }
  }
module.exports = logger;

