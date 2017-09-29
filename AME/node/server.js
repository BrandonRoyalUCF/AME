var express = require('express');
var app = express();
var bodyparser = require('body-parser');
var mongoose = require('mongoose');
var jwt = require('jsonwebtoken');

//Controllers
var dataController = require("./controllers/data-controller.js");
var authenticateController = require("./controllers/authenticate-controller.js");

app.use(bodyparser.urlencoded({limit: '16mb', extended: true}));
app.use(bodyparser.json({limit: '16mb'}));

var config = require('./config.js');
config.setConfig();

mongoose.connect(process.env.MONGOOSE_CONNECT);

app.listen(3000, function(){
    console.log('listening on 3000')
})

var clientSocket = null;

var secureRoutes = express.Router();

//API Calls

//Routers

app.use('/secure-api', secureRoutes);

secureRoutes.use((req, res, next) =>{
    
    console.log("secure request made")
    
	var token = req.body.token || req.headers['token'] || req.query["token"];
    
    console.log(token);

	if(token){
		jwt.verify(token, process.env.SECRET_KEY, (err, decoded) => {
            
			if(err){
				res.status(500).send('Invalid Token');
			}else{
                
                req.decoded = decoded;
                
                if(clientSocket){
                    req.socket = clientSocket;
                }
                
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


//READ

app.get('/key', dataController.getKey)
secureRoutes.get('/instructor', dataController.getInstructor);

//UPDATE

//DELETE