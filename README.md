# GymSy
## Requirements
Flask,

DateTime,

time

## Key Terms
### render_template(File,data)
The render tempalte sends html to the user's browser

### app.redirect(Link,Code)
The redirect sends a user to the link with a html code

### session[x]
This stores user data



# Files

## Main Directory
### app.py
This stores all the running code, it takes the link from the user, then it runs the code associated with the link. It returns either HTML code or a redirect to the user.

### README.md
Stores the data for this text


## Database
### DatabaseHandler.py
This is the script that contains all the functions for modifying the database

### GymsyDatabase.db
This is the database for the main code, this is kept on the server

### GymsyDatabaseTemplate.db
Incase there is an issue with the main database and code, this is a database backup with all database parts

### SqlCommands.py
This contains SQL Code and the Query() Class

### TimeFormatter.py
This just gets the time and gets the date in a format for SQL


## Templates
This contains all the HTML Code for the websites


## Templates/Static
This contains the Images,Scripts and styles

## Templates/Static/Images
### Favicon.ico
This contains the small icon at the top of the website

### search_icon.png
This is the icon used in the search bar


## Templates/Static/Scripts
### ExcersiseListConstructor.js
This is used in the excersise list to create each TomSelect for the excersise routine so it is appendable

### PopUp.js
This just opens the pop ups to login

### Redirect.js
This is used on any page with a post box to be able to redirect the user when thye click blank space on the post

### SendRequests.js
This sends data back and forth to the server

### Sidebar.js
This controls the sidebar and makes it expand and dispand on click


## Template/Scripts/Styles
### Style.css
This makes the html look pretty
