module.exports.setConfig = function(){
    process.env.MONGOOSE_CONNECT = "mongodb://localhost:27017/test"
    process.env.SECRET_KEY = "mykey"
}