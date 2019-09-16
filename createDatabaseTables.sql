------------------------------drop table if exists Professor;
create table Professor (
       ProfId INT AUTO_INCREMENT PRIMARY KEY,
       LName  	        VARCHAR(25),
       FName  	        VARCHAR(50),
       PEmail  	        VARCHAR(40),
       Department       VARCHAR(100)
);

drop table if exists Course;
create table Course (
       CSID	        VARCHAR(30),
       CName  	        VARCHAR(200),
       CNum  	        VARCHAR(15),
       Semester         VARCHAR(15)
);

drop table if exists Help;
create table Help (
       HelpID	        VARCHAR(50),
       Type  	        VARCHAR(25),
       HName  	        VARCHAR(50)
);

drop table if exists TA;
create table TA (
       TEmail	        VARCHAR(40),
       LName  	        VARCHAR(25),
       FName  	        VARCHAR(25)
);

drop table if exists Location;
create table Location (
       LocID	        VARCHAR(100),
       Building  	VARCHAR(25),
       Room  	        VARCHAR(10)
);

drop table if exists Teaches;
create table Teaches (
	ProfId INT,
	CSID  	        VARCHAR(30)
);

drop table if exists Has_Help;
create table Has_Help (
	CSID  	        VARCHAR(30),
	HelpID  	        VARCHAR(50)
);

drop table if exists Happens_In;
create table Happens_In (
	HelpID          VARCHAR(50),
	DayTime         VARCHAR(100),
	LocID  	        VARCHAR(100)
);

drop table if exists TA_OH;
create table TA_OH (
	TEmail          VARCHAR(40),
	CSID  	        VARCHAR(30),
	DayTime         VARCHAR(300),
	LocID  	        VARCHAR(100)
);

drop table if exists Works_For;
create table Works_For (
	TEmail          VARCHAR(40),
	CSID  	        VARCHAR(30)
);

drop table if exists Prof_OH;
create table Prof_OH (
	CSID  	        VARCHAR(30),
	DayTime         VARCHAR(200),
	LocID  	        VARCHAR(100)
);

drop table if exists Exam_Data;
create table Exam_Data (
	CSID  	        VARCHAR(30),
    Date             VARCHAR(50),
	Time         VARCHAR(200),
	Name  	        VARCHAR(100)
);

drop table if exists Assignment_Data;
create table Assignment_Data (
	CSID  	        VARCHAR(30),
    Date             VARCHAR(50),
	Name  	        VARCHAR(100)
);

drop table if exists Class_Times;
create table Class_Times (
	CSID  	        VARCHAR(30),
	DayTime         VARCHAR(200),
	LocID  	        VARCHAR(100),
    TYPE            VARCHAR(100)
);

"AS.100.268", "Fall 2018"
