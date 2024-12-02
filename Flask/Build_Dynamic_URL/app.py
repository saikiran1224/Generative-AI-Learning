# Building URL dynamically

from flask import Flask, redirect, url_for

app = Flask(__name__)

# homepage
@app.route("/")
def welcome():
    return ("Hi, I am Sai Kiran!")

# Using VARIABLE RULES method by passing the data in the URL itself.

# Success page
# In the URL itself, we will have the "score" value in form of int datatype.
@app.route("/success/<int:score>")
def success(score):
    return "The person has passed and the marks is " + str(score)

# Fail page
# In the URL itself, we will have the "score" value in form of int datatype.
@app.route("/fail/<int:score>")
def fail(score):
    return "The person has failed and the marks is " + str(score)

# Result checker - Redirects the page based on the condition.
@app.route("/results/<int:score>")
def results(score):

    result=""

    if score > 50:
        result = 'success' # storing the success page route name
    else: 
        result = 'fail' # storing the fail page route name

    return redirect(url_for(result,score=score)) # redirects based on result variable, and the score parameter will be passed. 

if __name__ == "__main__":
    app.run(debug=True)