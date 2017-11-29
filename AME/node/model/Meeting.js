var mongoose = require('mongoose');

mongoose.Promise = global.Promise;

module.exports = mongoose.model('Meeting', {
    dateTime: String,
    meetingPicAttachment_id: String,
    labeledMeetingPicAttachment_id: String,
    depthPicAttachment_id: String,
    attendance: [{student_id: String, present: Boolean}],
    croppedPics: [{student_id: String, croppedPicAttachment_id: String}],
    socialData: [{student_id: String, 
                  relationships: [{student_id: String, value: Number}]}],
    section_id: String
})