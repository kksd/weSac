var MongoClient = require('mongodb').MongoClient;


var dataImporter = function(){
    var self = this;

    this.hello = function(){
        // Connect to the db
        MongoClient.connect("mongodb://localhost:27017/exampleDb", function(err, db) {
          if(!err) {
            console.log("We are connected");
          }
        });
    }
    
}

module.exports = dataImporter;

