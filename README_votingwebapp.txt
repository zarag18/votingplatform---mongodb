StarVote Web Application:
StarVote is a voting system web application designed to allow users to cast their votes for 
their favorite actors in three different categories: best director, best male actor, 
and best female actor. Users can view the voting results for each category, and only 
logged-in users can place votes.

Database:
StarVote uses MongoDB as its database backend. 
The database contains a collection named votes where votes are stored and tallied, and a 
collection Users where users who registered are stored. When a user votes, the database stores 
their username, the category item they voted for, and the total number of votes that category 
item has.

Authentication:
Authentication in StarVote is handled by Django's built-in administration system. 
A superuser can log in to the administration panel to view all registered users, 
manage candidates, track voter activity, and edit category descriptions. Users must be logged 
in to vote, and Django's authentication libraries are used for this purpose. Email validation 
is implemented using Django's email validation library to verify the email addresses provided 
during registration.

Guest Access:
Guests do not need to log in or register and can view the results of the votes.

Voter Access:
Voters can view their results after casting a vote.

Data Validation
StarVote enforces several data validation measures:

Password matching
Password strength requirements
Incorrect password handling
Users can only vote once in a category
Users must be logged in to vote
Display of an error message for unsuccessful logins
Email Address must in the correct format for verification

Polling Results:
The polling results feature measures the percentage of votes for a specific 
category item compared to the total number of votes cast in that category.

Coding Structure:
mongodb.py: Configuration file for the MongoDB database.
models.py: Defines the Category and CategoryItem classes, and also stores the database collections.
views.py: Contains functions for all web pages. Each function returns its respective HTML page located 
in the templates folder. The views.py page is responsible for all the functionality of the webapp. It connects
 to the MongoDB database and inherits the database collections defined in the models.py file. The views.py file also 
 inherits classes defined in models.py when creating functions.
urls.py: Defines the paths for different pages and maps functions from views.py to their respective URLs.