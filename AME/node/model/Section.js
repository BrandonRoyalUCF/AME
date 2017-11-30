var mongoose = require('mongoose');

mongoose.Promise = global.Promise;

module.exports = mongoose.model('Section', {
    sectionID: String,//Ex: BSC2010-0001
    courseName: String,
    students: [{name: String, studentID: String, _id: String}],//"lastName, firstName" , _id
    socialData: [{student_id: String, 
                  relationships: [{student_id: String, value: Number}]}],
    meetings: [{dateTime: Number, _id: String}]
});