var jwt = require('jsonwebtoken');
var mongoose = require('mongoose');
const exec = require('child_process').exec;
var fs = require("fs");

var gridfs = require('mongoose-gridfs')({
    collection:'attachments',
    model:'Attachment',
    mongooseConnection: mongoose.connection
})

var Instructor = require('../model/Instructor.js');
var Section = require('../model/Section.js');
var Meeting = require('../model/Meeting.js');
var Student = require('../model/Student.js');
var Attachment = gridfs.model;

//////////////////////////////////////////////////////////////////////////////////////////
//HELPER FUNCTIONS
//////////////////////////////////////////////////////////////////////////////////////////

function sendToken(res, package) {
    
    var body = {};
    
    var token = jwt.sign(body, process.env.SECRET_KEY, {
		expiresIn: 4000
	});
    
    var json = {
		success: true,
		token: token,
        package: package
    };
    
    console.log('sending: ' + JSON.stringify(json, null, 2));

	res.json(json);
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
                                  studentPortrait: Buffer.from(req.body.studentPortrait, 'base64'),
                                  socialData: []});
    
    newStudent.save(function (err, student) {
        
        console.log('adding student to ' + req.body.sectionID);
    
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
                                  meetingPic: Buffer.from(meetingPic, 'base64'),
                                  attendance: [],
                                  croppedPics: [],
                                  section_id: section_id});
                                  
    newMeeting.save(function(err, meeting){
        if (err){
            console.log(err)
            return res.status(500).send('could not save');
        }
        
        var sectionText = '{\\"meeting_id\\":\\"' + meeting._id + '\\", ';

        Section.findOne({_id: section_id}, function(err, section) {
            if(err){
                console.log(err);
                return res.status(500).send("not werking");
            }

            sectionText.concat('[');
            
            for( i = 0; i < section.students.length; i++ ){

                Student.findOne({_id: section.students[i]._id}, function(err, student){
                    if(err){
                        console.log(err);
                        return res.status(500).send("not werking");
                    }

                    sectionText.concat('{\\"student_id\\":\\"' + student._id + '\\"}');

                    if(i != section.students.length - 1){
                        sectionText.concat(',');
                    }
                })
            }
            sectionText.concat(']}');
        })
        
        console.log(sectionText);
        
        const process = exec('C:/Users/Administrator/AppData/Local/Programs/Python/Python36/python C:/AME/AME/python/imgProc/match.py ' + sectionText, function (err, stdout, stderr){
            if (err){
                console.log(err)
            }
            if (stderr) {
                console.log(stderr)
            }
            
            console.log(stdout)
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
    
    var studentID = req.query["studentID"];
    
    Section.findOne({studentID: studentID}, function(err, student) {
        if(err){
            return res.status(500).send("not werking");
        }
        
        res.send(student);
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