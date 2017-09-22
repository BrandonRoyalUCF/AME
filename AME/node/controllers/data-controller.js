var jwt = require('jsonwebtoken');

var Instructor = require('../model/Instructor.js');
var Section = require('../model/Section.js');
var Meeting = require('../model/Meeting.js');
var Student = require('../model/Student.js');

//////////////////////////////////////////////////////////////////////////////////////////
//HELPER FUNCTIONS
//////////////////////////////////////////////////////////////////////////////////////////

function sendToken(res, body) {
    
    console.log('send token with body:' + body.toString());
    
    var token = jwt.sign(body, process.env.SECRET_KEY, {
		expiresIn: 4000
	});

	res.json({
		success: true,
		token: token
	});
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
        
        if(existingInstructor.length == 0){
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
    
    newSection.save(function(err){
        if(err){
            res.status(500).send("could not save");
        }
        
        var username = req.decoded.username
    
        Instructor.findOne({'username': username}, function(err, instructor){
            if (err){
                res.status(500).send("could not save");
            }

            var sections = instructor.sections;

            sections.push(req.body.sectionID);

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
                    req.body.studentPortrait = Buffer.from(students[i].studentPortrait, 'base64');
                    
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
                                  studentPortrait: req.body.studentPortrait,
                                  socialData: []});
    
    newStudent.save();
    
    console.log('adding student to ' + req.body.sectionID);
    
    Section.findOne({'sectionID': req.body.sectionID}, function(err, section){
        if (err){
            res.status(500).send('could not save');
        }
        
        var students = section.students;
        
        students.push(req.body.studentID);
        
        section.students = students;
        
        section.save();
    })
}

module.exports.postMeeting= function (req, res) {
    
    var meetingPic = Buffer.from(req.body.meetingPic, 'base64');
    
    req.socket.emit('newMeeting', meetingPic, function(string){
        console.log(string);
        
    })
    
}
//////////////////////////////////////////////////////////////////////////////////////////
//READ
//////////////////////////////////////////////////////////////////////////////////////////

module.exports.getKey= function(req, res) {
    console.log('sent key')
    res.send(process.env.SECRET_KEY)
}

module.exports.getInstructor = function(req, res) {
    
    var username = req.query["username"];
    
    console.log('getting' + username);
    
    //TODO GetInstructorById
    Instructor.find({username: username}, function(err, instructor) {
        if (err){
            return res.status(500).send("not werking");
        }
        
        res.send(instructor);
    });
};

module.exports.getSection = function(req, res) {
    
    var sectionID = req.query["sectionID"];
    
    Section.findOne({sectionID: sectionID}, function(err, section) {
        if(err){
            return res.status(500).send("not werking");
        }
        
        res.send(section);
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