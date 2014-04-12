exports.bind = function(app){
    var roomKeeper = app.get('roomKeeper');
    app.get('/createroom', function(req, res){
        res.send('welcome');
    });
};