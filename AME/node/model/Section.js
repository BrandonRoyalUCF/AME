var mongoose = require('mongoose');

mongoose.Promise = global.Promise;

module.exports = mongoose.model('Section', {
    sectionID: String,//Ex: BSC2010-0001
    courseName: String,
    students: [{name: String, studentID: String, _id: String}],//"lastName, firstName" , _id
    meetings: [{dateTime: String, _id: String}]
});