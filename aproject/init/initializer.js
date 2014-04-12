var router = require('./router');

exports.initialize = function (app, cb) {
    router.bind(app, function (err) {
        if (err) {
            console.log('Router initialization failed: ' + err);
            console.log(err.stack);
            cb(err);
        }
        else {
            //--> need to initialize database here and apply db patches
            console.log('router init done');
            cb();
        }
    });
};

/* Detailed Steps */
