INSERT INTO persons VALUES ('Fname1', 'Lname1', '1998-01-01', 'City1', 'Address1', 000000001);
INSERT INTO persons VALUES ('Fname2', 'Lname2', '1998-02-13', 'City1', 'Address2', 000000002);
INSERT INTO persons VALUES ('Fname3', 'Lname3', '1998-03-19', 'City1', 'Address3', 000000003);

INSERT INTO users VALUES ('person1', 'pass1', 'a', 'Fname1', 'Lname1', 'City1');
INSERT INTO users VALUES ('person2', 'pass2', 'o', 'Fname2', 'Lname2', 'City1');
INSERT INTO users VALUES ('person3', 'pass3', 'p', 'Fname3', 'Lname3', 'City1');  

INSERT INTO vehicles VALUES ('001', 'Make1', 'Model1', 2001, 'Black');
INSERT INTO vehicles VALUES ('002', 'Make2', 'Model2', 2002, 'Black');
INSERT INTO vehicles VALUES ('003', 'Make3', 'Model3', 2003, 'Black');
INSERT INTO tickets VALUES (123, 100, 250, 'Violatio1', '2007-10-10' );
INSERT INTO tickets VALUES (124, 100, 300, 'Violation2', '2006-10-10' );
INSERT INTO tickets VALUES (125, 100, 250, 'Violation3', '1996-10-10' );
INSERT INTO tickets VALUES (126, 100, 300, 'Violation4', '2004-10-10' );
INSERT INTO tickets VALUES (127, 100, 250, 'Violation5', '1998-10-10' );
INSERT INTO tickets VALUES (128, 100, 250, 'Violation6', '2002-10-10' );
INSERT INTO tickets VALUES (129, 100, 300, 'Violation7', '2001-10-10' );
INSERT INTO demeritNotices VALUES ('2000-08-19', 'Fname2', 'Lname2', 7, 'speeding');
INSERT INTO demeritNotices VALUES ('2001-08-19', 'Fname2','Lname2', 3, 'slow');
INSERT INTO demeritNotices VALUES ('2018-08-19', 'Fname2', 'Lname2', 11, 'x');
INSERT INTO demeritNotices VALUES ('2017-12-12', 'Fname2','Lname2', 4, 'y');
INSERT INTO demeritNotices VALUES ('2005-08-19', 'Fname3', 'Lname3', 5, 'else');
 
INSERT INTO registrations VALUES (100, '2000-08-19', '2001-08-19', 'Plate3', '001', 'Fname1', 'Lname1');


INSERT INTO payments VALUES (123, '2001-08-19', 50);
INSERT INTO payments VALUES (123, '2000-08-19', 50);