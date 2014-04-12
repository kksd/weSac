exports.bind = function (app) {
    var roomKeeper = app.get('roomKeeper');
    app.get("/", function(req, res){
        res.send('/poker1');
    });
};