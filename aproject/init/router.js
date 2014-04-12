var fs = require('fs');
var path = require('path');
var controllersFolder = path.resolve('./core/controllers');
var apisFolder = path.resolve('./core/apis');

exports.bind = function (app, cb) {
    try {
        //bind controllers
        var controllers = fs.readdirSync(controllersFolder);
        for (var i = 0; i < controllers.length; i++) {
            var filePath = path.join(controllersFolder, controllers[i]);
            if (filePath.lastIndexOf('.js') == filePath.length - 3) {
                var controller = require(filePath);
                controller.bind(app);
            }
        }
        //bind apis
        var apis = fs.readdirSync(apisFolder);
        for (var i = 0; i < apis.length; i++) {
            var filePath = path.join(apisFolder, apis[i]);
            if (filePath.lastIndexOf('.js') == filePath.length - 3) {
                var api = require(filePath);
                api.bind(app);
            }
        }

        cb();
    }
    catch (err) {
        cb(err);
    }
}