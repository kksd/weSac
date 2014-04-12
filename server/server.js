var routes = require('rapid-rest')();
// This module is for calculation
var Responder = require("./routes/responder.js");
var responder = new Responder();
var Importer = require("./tools/dataImporter.js");
var importer = new Importer();

var port = 4444;

routes('/:id')
    ('get', function(req, res, params){
        obj = {id: params.id};
        send(res, obj);
    });

function send(res, obj){
    res.writeHead(201, '', {'Content-Type': 'text/json'});
    res.end(JSON.stringify(obj));
}

routes.listen(port);