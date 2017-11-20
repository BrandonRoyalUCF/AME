var mongoose = require('mongoose');
var fs = require("fs");

var gridfs = require('mongoose-gridfs')({
    collection:'attachments',
    model:'Attachment',
    mongooseConnection: mongoose.connection
})

//Models
var Instructor = require('C:/AME/AME/node/model/Instructor.js');
var Section = require('C:/AME/AME/node/model/Section.js');
var Meeting = require('C:/AME/AME/node/model/Meeting.js');
var Student = require('C:/AME/AME/node/model/Student.js');
var Attachment = gridfs.model;

mongoose.connect("mongodb://localhost:27017/test");

mongoose.connection.on('open', function(){
    console.log('check')
    mongoose.connection.dropDatabase(function(err, result){
        console.log('db dropped')
        
        //load populate.json
        var contents = fs.readFileSync("populate.json");
        var jsonContent = JSON.parse(contents);
        
        //console.log(JSON.stringify(jsonContent, null, 2))        
        //add instructor
        for(i = 0; i < jsonContent.instructors.length; i++){
            var newInstructor = new Instructor({
                username: jsonContent.instructors[i].username,
                password: jsonContent.instructors[i].password,
                firstName: jsonContent.instructors[i].firstName,
                lastName: jsonContent.instructors[i].lastName,
                email: jsonContent.instructors[i].email,
                facultyID: jsonContent.instructors[i].facultyID,
                sections: []});
                                            
            newInstructor.save(function(err, instructor){
                if (err){
                    console.log(err)
                }
                
                    console.log('Added Instructor: ' + newInstructor)
                    
                    //add section
                    for(i = 0; i < jsonContent.sections.length; i++){
                        var newSection = new Section({
                            sectionID: jsonContent.sections[i].sectionID,
                            courseName: jsonContent.sections[i].courseName,
                            students: [],
                            meetings: []});
                    
                        newSection.save(function(err, section){
                            if (err){
                                console.log(err)
                            }
                            
                            instructor.sections.push({name: section.sectionID,
                                                _id: section._id});
                            
                            instructor.save()
                            
                            console.log('Added Section: ' + newSection)
                            
                            //add students without pictures
                            for(i = 0; i < jsonContent.students.length; i++){
                                var newStudent = new Student({
                                    firstName: jsonContent.students[i].firstName,
                                    lastName: jsonContent.students[i].lastName,
                                    studentID: jsonContent.students[i].studentID,
                                    studentPortrait: jsonContent.students[i].studentPortrait,
                                    socialData: []});
                            
                                newStudent.save(function(err, student){
                                    if (err){
                                        console.log(err)
                                    }
                                    
                                    console.log('Added Student: ' + student)
                                    
                                    section.students.push({
                                    name: student.lastName + ", " + student.firstName,
                                    studentID: student.studentID,
                                    _id: student._id});
                                    section.markModified('students')
                                    
                                    if(section.students.length == jsonContent.students.length){
                                        section.save()
                                    }
                                    
                                });
                            }
                        });
                    }
                });
            }
        
        //add pictures based on firstName
        for(i = 0; i < jsonContent.students.length; i++){
            //console.log("uploading pic at C:/AME/AME/node/CroppedFaces/" + (i+1) + ".png")
            
            fs.readFile("C:/AME/AME/node/CroppedFaces/" + (i+1) + ".png", function(err, data){
                Student.updateOne({firstName: (i+1) + ""}, 
                                  {studentPortrait: Buffer.from(data.toString())},
                                  function(err, affected, resp){
                    
                })
            });
        }
    })
})


