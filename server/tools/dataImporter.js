var MongoClient = require('mongodb').MongoClient;
var fs = require('fs');


var PATH_TO_RAW_DATA_FILE_FOLDER = './raw/';


var dataImporter = function(){
    var self = this;
    var subjectList = new Array();
    console.log(subjectList);

    this.hello = function(){
        // Connect to the db
        MongoClient.connect("mongodb://localhost:27017/exampleDb", function(err, db) {
          if(!err) {
            var collection = db.collection('data');
            var doc1 = {'hello':'doc1'};
            collection.insert(doc1, {w:1}, function(err, result) {
                if(err){
                    console.log(err);
                } else {
                }
            });
          } else {
                    console.log(err);
                 }
        });
    }

    this.getRawDataList = function(callback){
        fs.readdir(PATH_TO_RAW_DATA_FILE_FOLDER, function(err, files){
            subjectList = files;
            // console.log(subjectList);
            callback();
        })
    }

    this.getSubjectInformation = function(){
        console.log(subjectList);
        for(var i = 0; i < subjectList.length; i++){
            console.log("loading subject " + i);
            fs.readFile(PATH_TO_RAW_DATA_FILE_FOLDER + subjectList[i],
                        'utf8', 
                        function (err, data) {
                                    if (err) throw err;
                                    var tokens = data.split('[*]')
                                    raw_info = tokens[1];
                                    raw_attr = tokens[2];
                                    raw_orbit = tokens[3];
                                    self.parseRawInfo(raw_info);
                                    // console.log(raw_info);
                                });
        }
    }

    this.parseRawInfo = function(raw){
        console.log(raw);
        var info_set = raw.split('\n');
        console.log(info_set.length);
    }
    
}

module.exports = dataImporter;

