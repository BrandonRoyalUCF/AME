var mongoose = require('mongoose');

mongoose.Promise = global.Promise;

module.exports = mongoose.model('Meeting', {
    dateTime: String,
    meetingPic: Buffer,
    attendance: [{student: String, present: Boolean}],
    croppedPics: [{student: String, pic: Buffer}],
    section: String
})