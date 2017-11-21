var mongoose = require('mongoose');

mongoose.Promise = global.Promise;

module.exports = mongoose.model('Meeting', {
    dateTime: String,
    meetingPicAttachment_id: String,
    attendance: [{student: String, present: Boolean}],
    croppedPics: [{student: String, pic: Buffer}],
    section_id: String
})