Base Skeleton to start your application using Flask-AppBuilder
--------------------------------------------------------------

# Set-up it :
```
  - viretualenv venv
  - . venv/bin/activate # to activate virtual environment
  - git clone https://github.com/devketanpro/home_assignment.git
  - cd home_assignment/movie
```
# Install it:
```
- pip install -r requirements.txt
```

# Create admin user
```
- flask fab create-admin
# Provide username, first name, last name, email, password and confirm password.

```

# Run it:

Command to run the flask application
```
- flask run
```
Now you can go to the http://127.0.0.1:5000 on your local browser to check the functionality. 
You can log in as a admin user. In the header section you can see two drop down.
- Movie detail
 
    onclick Fetch Movies link appear on click Fetch Movie you can fetch movie date from given url.
    This may take a little time to fetch large amount of movie data.
  - Movie detail list

    onclick Fetch Movies link appear on click List Groups you can see list of movies data stored in database.


Command to  run test case
```
- python -m unittest
```
That's it!!
