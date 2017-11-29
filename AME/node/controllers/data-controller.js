var jwt = require('jsonwebtoken');
var mongoose = require('mongoose');
const exec = require('child_process').exec;
var fs = require("fs");

var gridfs;

var Instructor = require('../model/Instructor.js');
var Section = require('../model/Section.js');
var Meeting = require('../model/Meeting.js');
var Student = require('../model/Student.js');
var Attachment;

mongoose.connection.on('open', function(){
    gridfs = require('mongoose-gridfs')({
        collection:'attachments',
        model:'Attachment',
        mongooseConnection: mongoose.connection
    })
    
    gridfs.model;

})

//////////////////////////////////////////////////////////////////////////////////////////
//HELPER FUNCTIONS
//////////////////////////////////////////////////////////////////////////////////////////

function sendToken(res, package) {
    
    console.log('send token with package:' + package.toString());
    
    var token = jwt.sign({}, process.env.SECRET_KEY, {
		expiresIn: 4000
	});

	res.json({
		success: true,
		token: token,
        package: package
	});
}

function bufferToStream(buffer) {  
  let stream = new Duplex();
  stream.push(buffer);
  stream.push(null);
  return stream;
}


//////////////////////////////////////////////////////////////////////////////////////////
//CREATE
//////////////////////////////////////////////////////////////////////////////////////////

module.exports.postInstructor = function(req, res) {
    
    //TODO  encrypt password
    var newInstructor = new Instructor({username: req.body.username,
                                        password: req.body.password,
                                        firstName: req.body.firstName,
                                        lastName: req.body.lastName,
                                        email: req.body.email,
                                        facultyID: req.body.facultyID,
                                        sections: []});
    
    Instructor.findOne({'username': newInstructor.username}, function(err, existingInstructor) {
        if (err){
            res.status(500).send("could not save");
        }
        
        console.log(existingInstructor)
        
        if(existingInstructor == null){
            newInstructor.save(function(err){
                if (err){
                    res.status(500).send("could not save");
                }
                
                console.log('Added: ' + newInstructor)
            
                sendToken(res, {})
            });
        }
    });
};

module.exports.postSection = function(req, res) {
    
    console.log('making new section: ' + req.body.sectionID)
    
    var newSection = new Section({sectionID: req.body.sectionID,
                                  courseName: req.body.courseName,
                                  students: [],
                                  meetings: []});
    
    newSection.save(function(err, section){
       
 if(err){
            res.status(500).send("could not save");
        }
        
        var username = req.decoded.username
    
        Instructor.findOne({'username': username}, function(err, instructor){
            if (err){
                res.status(500).send("could not save");
            }

            var sections = instructor.sections;

            sections.push({name: req.body.sectionID,
                           _id: section._id});

            instructor.sections = sections;

            instructor.save();
            
            students = JSON.parse(req.body.students);
            
            for(i in students){
                
                console.log(students[i].firstName);
                console.log(students[i].lastName);
                console.log(students[i].studentID);
                
                if(students[i].firstName){
                    
                    req.body.firstName = students[i].firstName;
                    req.body.lastName = students[i].lastName;
                    req.body.studentID = students[i].studentID;
                    req.body.studentPortrait = students[i].studentPortrait;
                    
                    console.log(req.body.studentPortrait);
                
                    module.exports.postStudent(req, res);
                }
            }
        })
    })
}

module.exports.postStudent = function (req, res) {
    
    
    
    var newStudent = new Student({firstName: req.body.firstName,
                                  lastName: req.body.lastName,
                                  studentID: req.body.studentID,
                                  studentPortraitAttachmentId: '',
                                  socialData: []});
    
    newStudent.save(function (err, student) {
        
        console.log('adding student to ' + req.body.sectionID);
        
        Attachment.write({
            filename: student._id + '.jpg',
            contentType: 'image/jpg'
            },
            bufferToStream(Buffer.from(req.body.studentPortrait)),
            function(error, createdFile){
                student.studentPortraitAttachment_id = createdFile._id;
                student.save();
            }   
        )
        
        Section.findOne({'sectionID': req.body.sectionID}, function(err, section){
            if (err){
                return res.status(500).send('could not save');
            }

            var students = section.students;

            students.push({name: student.lastName + ", " + student.firstName,
                           studentID: student.studentID,
                           _id: student._id});

            section.students = students;

            section.save();
        })
    });
}

module.exports.postMeeting= function (req, res) {
    
    console.log('postMeeting called');

    var section_id = req.body.section_id;

    var meetingPic = req.body.meetingPic.toString()
    
    var newMeeting = new Meeting({dateTime: 0,
                                  meetingPicAttachment_id: '',
                                  attendance: [],
                                  croppedPics: [],
                                  section_id: section_id});
                                  
    newMeeting.save(function(err, meeting){
        if (err){
            console.log(err)
            return res.status(500).send('could not save');
        }
        
        Attachment.write({
            filename: meeting._id + '.jpg',
            contentType: 'image/jpg'
            },
            bufferToStream(bufferToStream(Buffer.from(req.body.meetingPic)),
            function(error, createdFile){
                meeting.meetingPicAttachment_id = createdFile._id;
                meeting.save();
            })
        )
        
        meetingJSONString = '{\"meeting_id\": \"'+ meeting._id+'\",\"section_id\": \"'+ section_id+'\"}';
        
        const process = exec('C:/Users/Administrator/AppData/Local/Programs/Python/Python36/python C:/AME/AME/python/imgProc/match.py ' + meetingJSONString, function (err, stdout, stderr){
            if (err){
                console.log(err)
            }
            if (stderr) {
                console.log(stderr)
            }
            
            console.log(stdout)
            
            sendToken(res, stdout)
        });
    })
}

//////////////////////////////////////////////////////////////////////////////////////////
//READ
//////////////////////////////////////////////////////////////////////////////////////////

module.exports.getInstructor = function(req, res) {
    
    var username = req.query["username"];
    
    console.log('getting' + username);
    
    //TODO GetInstructorById
    Instructor.findOne({username: username}, function(err, instructor) {
        if (err){
            return res.status(500).send("not werking");
        }
        sendToken(res, instructor);
    });
};


module.exports.getSection = function(req, res) {
    
    var section_id = req.query["section_id"];
    
    var id = mongoose.Types.ObjectId(section_id);
    
    console.log("finding section with _id:  " + id);
    
    Section.findOne({_id: id}, function(err, section) {
        if(err){
            console.log(err)
            return res.status(500).send("not werking");
        }
        
        sendToken(res, section);
    })
}

module.exports.getStudent = function(req, res) {
    
    var student_id = req.query["student_id"];
    
    Student.findOne({_id: student_id}, function(err, student) {
        if(err){
            return res.status(500).send("not werking");
        }
        
        sendToken(res, student);
    })
}

module.exports.getMeeting = function(req,res) {
    
    var meetingID = req.query["meetingID"];
    
    Meeting.findOne({meetingID: meetingID}, function(err, meeting){
        if(err){
            return res.status(500).send("Not working");
        }
        
        res.send(meeting);
    })
}

///////////////////////////////////////////////////////////////////////////////////
//UPDATE
/////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////
//DELETE
//////////////////////////////////////////////////////////////////////////////////////////