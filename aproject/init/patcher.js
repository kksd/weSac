var fs = require('fs');
var path = require('path');
var logger = require('../tools/logger');
var patchFolder = path.resolve('patches');
var sysRepo = require('../data/repos/sysRepo');
var config = require('../config');
var Version = require('../models/version');
var prefix = config.patcher.prefix;

exports.patch = function (cb) {
    checkDB(cb);
};

/* Utilities */
function checkDB(cb){
    sysRepo.getVersion(function (err, version) {
        if (err) {
            cb(err);
            return;
        }

        if (version == null) {
            //db connection succeed, but this collection needs to be initialized
            //everything starts from 0
            version = new Version();
            version.sysVersion = 0;
            version.dbVersion = 0;
            version.patchDate = Date.now();
            sysRepo.updateVersion(version, function (err) {
                cb(err);
            });
        }
        else {
            //it's already there, can start applying patches
            //from next db version
            version.dbVersion = version.dbVersion + 1;
            apply(version, cb);
        }
    });
}

function apply(version, cb){
    var fileName = prefix + version.dbVersion + '.js';
    var filePath = path.join(patchFolder, fileName);
    if (fs.existsSync(filePath)) {
        var curPatch = require(filePath);
        curPatch.apply(function (err) {
            if (err) {
                logger.log('Patch ' + fileName + ' failed: ' + err);
                cb(err);
            }
            else {
                //update version in db
                sysRepo.updateVersion(version, function (err) {
                    if (err) {
                        console.log('However, version number in the DB cannot be updated, please fix manually.');
                    }
                    version.dbVersion = version.dbVersion + 1;
                    version.patchDate = Date.now();
                    apply(version, cb);
                });
            }
        });
    }
    else {
        //already hit the last one
        cb();
    }   
}