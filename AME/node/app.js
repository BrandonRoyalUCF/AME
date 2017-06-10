var https = require('https'),
    express = require('express'),
    bodyparser = require('body-parser'),
    mongoClient = require('mongodb').MongoClient
    
var url = 'mongodb://localhost:27017/'

var db = mongoClient.connect(url)
    
var app = express()

app.use(bodyparser.json())

app.listen(3000, function(){
    console.log('listening on 3000')
})

//Helper functions

//Generate Token with AES algorithm using timestamp that is passed in
function encryptTokenId(tokenId){
    //TODO perform AES on timstamp
    return tokenId
}

function generateTokenId(username, timestamp){
    
    var tokenId = parseInt(username, 10).toString + timestamp.toString
    
    tokenId = encryptTokenId(tokenId)
    
    return tokenId
}

//Used for Login and Registration
function getStartToken(username){
    
    
    //TODO add Token to Token Collection
    db.collection('tokens').insertOne(token)
    
    return token
}

function tokenIsNotExpired(tokenId){
    
    var token = getToken(tokenId)
    
    if(token.expiration < Date.now()){
        return false
    }
    
    return true
}

function getToken(token){
    
    
    if token['tokenId'] = 'null'{
        
        var timestamp = Date.now()
        
        tokenId = generateTokenId(username, timestamp)
        
        //Expriation time is timestamp + 15 minutes (.0001 * 1000 = 1 sec * 60 = 1 min * 15 = 15 min
        expiration = timestamp + 900000
        
        token = 
        {
            "tokenId" : tokenId,
            "username" : username,
            "expiration": expiration
        }
        
        db.collection('tokens').insertOne(token)
        
    }else{
        token = db.collection('tokens').find({'tokenId': tokenId})
        //Expriation time is timestamp + 15 minutes (.0001 * 1000 = 1 sec * 60 = 1 min * 15 = 15 min
        token['expiration'] = token['expiration'] + 900000
        
        db.collection('tokens').updateOne({'tokenId': token['tokenId']}, {'expiration': token[expiration]})
    }
    
    return token
}

//API Calls

//CREATE

//Register with username and password
app.post('/user', (req, res) => {
    
    console.log(req.body)
    
    //Extract userInfo from request body
    var firstName = req.body['firstName']
    var lastName = req.body['lastName']
    var email = req.body['email']
    var username = req.body['username']
    var password = req.body['password']
    
    //Add user info to Dictionary
    var user = {
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
        'username': username,
        'password': password,
        'sections': []
    }
    
    console.log(user['lastName'])
    
    //Add user to Database
    //db.collection('users').insertOne(user)
    
    res.send(getToken('null'))
})

//READ

app.get('/', (req, res) => {
    res.send('Hello World')
})

app.get('/user', (req, res) => {
    var token = req.body['token']
    
    if(tokenIsFresh(token){
        var username = token['username']
        
        var user = db.collection('users').findOne({'useranme': username})
        
        res.send(user)
    }
})

//UPDATE



//DELETE