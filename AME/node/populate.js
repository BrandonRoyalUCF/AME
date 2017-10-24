var mongoose = require('mongoose');

var Instructor = require('../model/Instructor.js');
var Section = require('../model/Section.js');
var Meeting = require('../model/Meeting.js');
var Student = require('../model/Student.js');

mongoose.connect("mongodb://localhost:27017");

