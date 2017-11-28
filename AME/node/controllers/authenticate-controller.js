var jwt = require('jsonwebtoken');

var Instructor = require('../model/Instructor.js');

function sendToken(res, package) {
    
    console.log('send token with package:' + package.toString());
    
    var token = jwt.sign({}, process.env.SECRET_KEY, {
		expiresIn: 4000
	});

	res.json({
		success: true,
		token: token,
        package: package
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