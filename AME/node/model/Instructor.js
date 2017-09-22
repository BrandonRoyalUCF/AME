var mongoose = require('mongoose');

mongoose.Promise = global.Promise;

module.exports = mongoose.model('Instructor', {
    username: String,
    password: String, //encrypted
    firstName: String,
    lastName: String,
    email: String,
    facultyID: String,
    sections: [{name: String, _id: String}]
});