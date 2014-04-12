exports.bind = function (app) {
    var roomKeeper = app.get('roomKeeper');
    app.get("/", function(req, res){
        res.send('/poker1');
    });

    app.get("/test123", function(req, res){
        res.send('response: test567');
    });


    app.get("/testjson123", function(req, res){
        res.send({'response': 'json456'});
    });
};