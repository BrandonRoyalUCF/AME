var mongoose = require('mongoose');
var fs = require("fs");



//Models
var Instructor = require('C:/AME/AME/node/model/Instructor.js');
var Section = require('C:/AME/AME/node/model/Section.js');
var Meeting = require('C:/AME/AME/node/model/Meeting.js');
var Student = require('C:/AME/AME/node/model/Student.js');


mongoose.connect("mongodb://localhost:27017/test");



mongoose.connection.on('open', function() {
    
    var gridfs = require('mongoose-gridfs')({
        collection:'attachments',
        model:'Attachment',
        mongooseCollection: mongoose.connection
    })

    var Attachment = gridfs.model;
    
    mongoose.connection.dropDatabase(function(err, result){
        console.log('data dropped');
        
        var contents = fs.readFileSync("populateFinal.json");
        var jsonContent = JSON.parse(contents);
        
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
                        
                        Attachment.write({
                            filename: "meetingPic.jpg",
                            contentType: 'image/jpg'
                            },
                            fs.createReadStream('C:/AME/AME/node/MeetingPic/meetingPic.jpg'),
                            function(error, meetingPic){
                                Attachment.write({
                                    filename: "depthPic.jpg",
                                    contentType: 'image/jpg'
                                    },
                                    fs.createReadStream('C:/AME/AME/node/MeetingPic/depthPic.jpg'),
                                    function(error, depthPic){
                                        /*var newMeeting = new Meeting({
                                            dateTime: '',
                                            meetingPicAttachment_id: meetingPic._id,
                                            depthPicAttachment_id: depthPic._id,
                                            attendance: [],
                                            croppedPics: [],
                                            socialData: [],
                                            section_id: section._id
                                        })
                                        
                                        newMeeting.save(function(err, meeting){
                                            
                                        })*/
                                    }
                                )
                            }
                        )

                        //add students without pictures
                        for(i = 0; i < jsonContent.students.length; i++){
                            
                            var newStudent = new Student({
                                firstName: jsonContent.students[i].firstName,
                                lastName: jsonContent.students[i].lastName,
                                studentID: jsonContent.students[i].studentID,
                                studentPortraitAttachment_ids: []
                            });

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
                                Attachment.write({
                                    filename: (student.studentID) + "a.jpg",
                                    contentType: 'image/jpg'
                                    },
                                    fs.createReadStream('C:/AME/AME/node/CroppedFinalFaces/' + (student.studentID)+'a.jpg'),
                                    function(error, createdFileA){
                                        Student.updateOne({_id: student._id},
                                                          {$push: {studentPortraitAttachment_ids: createdFileA._id}},
                                                          function(err){
                                                              console.log(err)
                                                          })
                                    }
                                )
                            
                                Attachment.write({
                                    filename: (student.studentID) + "b.jpg",
                                    contentType: 'image/jpg'
                                    },
                                    fs.createReadStream('C:/AME/AME/node/CroppedFinalFaces/' + (student.studentID)+'b.jpg'),
                                    function(error, createdFileB){
                                        Student.updateOne({_id: student._id},
                                                          {$push: {studentPortraitAttachment_ids: createdFileB._id}},
                                                          function(err){
                                                              console.log(err)
                                                          })
                                    }
                                )
                                Attachment.write({
                                    filename: (student.studentID) + "c.jpg",
                                    contentType: 'image/jpg'
                                    },
                                    fs.createReadStream('C:/AME/AME/node/CroppedFinalFaces/' + (student.studentID)+'c.jpg'),
                                    function(error, createdFileC){
                                        Student.updateOne({_id: student._id},
                                                          {$push: {studentPortraitAttachment_ids: createdFileC._id}},
                                                          function(err){
                                                              console.log(err)
                                                          })
                                    }
                                )
                                

                            });
                        }
                    });
                }
            });
        }
    })
})