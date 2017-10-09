var mongoose = require('mongoose');

mongoose.Promise = global.Promise;

module.exports = mongoose.model('Student', {
    firstName: String,
    lastName: String,
    studentID: String,
    studentPortrait: Buffer,
    socialData: [{section: String, 
                  relationships: [{student: String, 
                                   strength: Number}] 
                 }]
});