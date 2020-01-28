# Registry-Database
 A database made in SQL so users can log in as Registry Agent or a Traffic Officer and update the database accordingly or query certain information whenever needed.
 
 This application uses python and SQL. 
 
## What I learned
* How to input and update data from the database tables
* How to integrate SQL into a python program
* How to query over the database and pull certain information to present to the user

## How to run
 To run the program the user must first enter ‘python3 prj1.py’ in the command line. After this the user will be prompted to enter the filename of the database. The system requests the user to login and based on their user type they are sent to the corresponding menu. The officer and registry agent menu will have a different options since each user type has different functionalities. We also added a menu option for a user who isn’t an officer or agent but their only options will be to logout or quit. Each menu option is provided with a logout and quit function. Once a user has chosen a valid option for the menu it will usually ask them for information so that a task can be initiated. The option to quit is also offered at anytime and no changes will be made to the database if the user chooses to quit. After a task is done the user will be prompted to choose to go back to the menu, logout, or quit.
