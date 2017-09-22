var mongoose = require('mongoose');

mongoose.Promise = global.Promise;

module.exports = mongoose.model('Section', {
    sectionID: String,
    courseName: String,
    students: [{name: String, studentID: String, _id: String}],//"lastName, firstName" , _id
    meetings: [{dateTime: String, _id: String}]
});