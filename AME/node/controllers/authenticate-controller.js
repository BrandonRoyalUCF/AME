var jwt = require('jsonwebtoken');

var Instructor = require('../model/Instructor.js');

function sendToken(res, body) {
    
    console.log('send token with body:' + body.toString());
    
    var token = jwt.sign(body, process.env.SECRET_KEY, {
		expiresIn: 4000
	});

	res.json({
		success: true,
		token: token
	});
}


module.exports.authenticate = function(req,res){
    
    var username = req.body.username.toString();
    //TODO  encrypt password
    var password = req.body.password.toString();
    
    console.log("login attempted for: " + username + ", " + password)
    
    
    Instructor.findOne({username: username}, function(err, instructor) {
        if (err){
            return res.status(500).send("not werking");
        }
        
        
        dbpassword = instructor.password.toString();
        
        console.log(dbpassword);
        
        if(instructor != null){
            if(dbpassword == password){
               sendToken(res, {username: username})
            }else{
                return res.status(500).send("bad user/pass combo");
            }
        }
        
        
        
    });

	
}