const router       = require('router')();
const finalhandler = require('finalhandler');

const users = [
  {id: 0, name: "Andreas"},
  {id: 1, name: "Martin"},
  {id: 2, name: "Lars"},
  {id: 3, name: "Jarle"},
  {id: 4, name: "Ken"},
  {id: 5, name: "Frode"},
]

module.exports = function(req, res) {
  router(req, res, finalhandler(req, res));
};

router.get('/users', function(req, res){
  res.statusCode = 200;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.json(users)
});

router.get('/users/:id', function(req, res){
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  const user = users[req.params.id]
  if (user) {
    return res.json(user)
  }
  res.statusCode = 404
  res.json({message: 'user not found', code: 404})
});
