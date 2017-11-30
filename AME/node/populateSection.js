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
        
        var contents = fs.readFileSync("populateSmall.json");
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

                    });
                }
            });
        }
    })
})