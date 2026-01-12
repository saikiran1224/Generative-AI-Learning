# Step - 1: importing flask library
from flask import Flask

# Step - 2: Creates a flask app object which is the WSGI application by passing the __name__ parameter.
app = Flask(__name__) 

# Step - 3: Creation of pages
# Below is a decorator which takes two parameters - rule and options
# @app.route(rule = '/', options) This statements binds the function written below
# rule - its the URL from where we want to access
# options - TBD

# Root homepage
@app.route(rule = '/') 
def welcome(): # This function will gets executed when we go the '/' in the website.
    return "Hi, Welcome to new world! I am in Bengaluru."

# Second homepage
@app.route(rule = '/profile') 
def profile_data(): # This function will gets executed when we go the '/profile' in the website.
    return "Hi, I am working in Accenture."

# statement written to check if the current program is being run as the MAIN PROGRAM.
# if this program is imported, then the __name__ will contain the name of module from where its imported.
if __name__ == '__main__':
    app.run(debug=True) # debug=True makes the server to get auto-started when the file is modified. 
