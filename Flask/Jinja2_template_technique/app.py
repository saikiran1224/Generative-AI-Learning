# Undderstanding Jinja2 template engine
# This helps us to display values in the HTML page, when it passed on to the render_template and url_for function using flask.

# Below are some important statements: 
'''

{% ... %} used for conditional statements, for loops

{{ variable name }} used for expressions to print output

{# ... #} used for displaying comments (which will not be rendered)

'''

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

# homepage - displaying index.html
@app.route("/")
def welcome():
    # Remember when we use render_template, it will check the file under templates folder
    # We are displaying form to enter marks for each subject and once submit button is clicked, it will navigate to '/submit' route.
    return render_template('index.html')

# Route gets invokes once the submit button is clicked.
# Fetches the data from the input fields, and computes the total score.
@app.route('/submit', methods=['POST','GET'])
def submit():

    total_score = 0

    if request.method == 'POST':
        science = float(request.form['science'])
        maths = float(request.form['maths'])
        c = float(request.form['c'])
        data_science = float(request.form['datascience'])

        total_score = (science + maths + c + data_science) / 4

    # once the total_score is calculated, we are re-directing to the results route along with the score acheived by the user,
    # where it will show the final response to user.
    return redirect(url_for('results', score = total_score))

# Once we get the re-direct along with the score, we will calculate the final response and pass the data to HTML page by parameter.
@app.route("/results/<int:score>")
def results(score):

    # calculating the condition
    result = "Pass" if score >= 50 else "Fail"
    
    # passing more than one parameter in form of dictionary to the HTML page
    exp = {'score': score, 'result': result}

    # Remember the parameter name displayed here should match in the HTML page.
    return render_template('result.html', exp = exp) 


if __name__ == "__main__":
    app.run(debug=True)