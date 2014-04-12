var routes = require('rapid-rest')();

var port = 4444;

routes('/:id')
	('get', function(req, res, params){
		obj = {id: params.id};
		res.writeHead(201, '', {'Content-Type': 'text/json'});
		res.end(JSON.stringify(obj));
	});

routes.listen(port);