var express = require('express');
var app = express();
var bodyparser = require('body-parser');
var mongoose = require('mongoose');
var jwt = require('jsonwebtoken');

//Controllers
var dataController = require("./controllers/data-controller.js");
var authenticateController = require("./controllers/authenticate-controller.js");

app.use(bodyparser.urlencoded({limit: '40mb', extended: true}));
app.use(bodyparser.json({limit: '40mb'}));

var config = require('./config.js');
config.setConfig();

mongoose.connect(process.env.MONGOOSE_CONNECT);

app.listen(3000, function(){
    console.log('listening on 3000')
})

var secureRoutes = express.Router();

//API Calls

//Routers

app.use('/secure-api', secureRoutes);

secureRoutes.use((req, res, next) =>{
    
    console.log("secure request made")
    
    
    
	var token = req.body.token || req.headers['token'] || req.query["token"];
    
    console.log('body: ' + token);
    console.log('headers: ' + token);
    console.log('query: ' + token);


	if(token){
		jwt.verify(token, process.env.SECRET_KEY, (err, decoded) => {
            
			if(err){
				res.status(500).send('Invalid Token');
			}else{
                
                req.decoded = decoded;
                
                console.log("next");
                
				next();
			}
		})
	}else{
		res.send('please send a token');
	}
});

//CREATE
app.post('/authenticate', authenticateController.authenticate);

app.post('/instructor', dataController.postInstructor);
secureRoutes.post('/section', dataController.postSection);
secureRoutes.post('/student', dataController.postStudent);
secureRoutes.post('/meeting', dataController.postMeeting);

//READ

secureRoutes.get('/instructor', dataController.getInstructor);
secureRoutes.get('/section', dataController.getSection);
secureRoutes.get('/meeting', dataController.getMeeting);
secureRoutes.get('/student', dataController.getStudent);

//UPDATE

//DELETE