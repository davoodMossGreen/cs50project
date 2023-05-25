# Book&I
#### Video Demo:  <https://youtu.be/s6ZWj9cr9pA>
#### Description:
Book&I is a web-service that lets its users to keep track of all the books of their interest whether those are the books they have already read or just plan to add to their booklists.
People can join the service and use its functionality: add and delete books, add and delete notes, to check when each specific book was added to their lists, to learn something new from "Editor's picks" section.
Project's code consists of several python, css, and html files. Let's break them down:
flask_session folder contains code that is neccessary for flask loading. Because we heavily rely on flask to implement many features of the website, this folder that contains five files is crucial to the project. Because of flask it became much easier to use such features as logging in and out, users' sessions - starting and finishing/clearing them.
static folder contains favicon file and styles.css file which is basically just a stylistic additional code to the existing HTML code and imported bootstrap code.
templates folder contains all the HTML files. Apart from basic HTML code there was also some data implemented from getbootstrap. Jinja template was also implemented in order to connect pythonic code with HTML files.
add.html - a page for uploading books - corresponds to /add in app.py
apology.html - a page that pops out when something goes wrong - corresponds to apology function in helpers.py
book.html - a page that a user can see wherever they add a new book, it contains a new book's info - corresponds to /book in app.py
deleteAccount.html - a page for deletting one's account - corresponds to /deleteAccount in app.py
deletebooks.html - a page where users can choose which books they wish to delete - corresponds to /deletebooks in app.py
history.html - a page with a list of timestamps when all the books were added - corresponds to /history in app.py
layout.html - speaks for itself
login.html - a page that prompts a username and a password from user in order to get access to service's functionaly - corresponds to /login in app.py
mybooks.html - a page where users can see all the books that they have added in the table with title, author, year of publishing, and description; there are also two links (add books and delete books) on this page - corresponds to /mybooks in app.py
notes.html - page with adding/deleting notes functionality - corresponds to /notes in app.py
register.html - a page where users can join the web-service - corresponds to /register in app.py
app.py is the main file of the project. It is written in python, imports data from flask. This file is fundamental to the project, contains its main functionality - log in/out, register, delete account, add books, delete books, add and delete notes.
helpers.py contains two helper functions - apology (page that pops up whenever something goes wrong) and login required (function that makes sure that only those whore logged in can have access to specific functionalities).
project.db is a SQL file that contains database of the project. It consists of 3 tables: users, notes, and books. Each of these tables include data on subjects corresponding to their names. Users: id, username, and hash. Notes: heading, text of the note, id, and date. Books: title, description, author, the year of publishing, timestamp, user's id, username.