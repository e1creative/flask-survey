from crypt import methods
from urllib import response
from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey 

app = Flask(__name__)

app.config['SECRET_KEY'] = "testingflask"
debug = DebugToolbarExtension(app)


@app.route("/")
def home():
    """Show our home page with title, instructions and start button"""

    return render_template("home.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)


@app.route("/", methods=["POST"])
def home_sessions():
    """Reset session"""
    session["responses"] = []

    print("*********** session ***********")
    print(session["responses"])
    print("----------- session -----------")

    return redirect("/questions/1")


@app.route("/questions/<int:question_num>")
def questions(question_num):
    """Show our question based on the url string"""

    print("*********** session ***********")
    print(session["responses"])
    print("----------- session -----------")

    referrer = request.referrer
    print(f"referrer url: {referrer}")


    # if there is no referrer (manually entered a url)
    if not referrer:
        # if we already have 4 responses, send them to the thank you page
        if len(session["responses"]) == 4:
            flash("You already have 4 responses")
            return redirect("/thankyou")

        # if we don't have 4 responses, send them to the next question page
        send_back_to_question_num = str(len(session["responses"])+1)
        send_back_to_question_path = f"/questions/{send_back_to_question_num}"
        flash("Please answer the questions in order")
        return redirect(send_back_to_question_path)

    # the index of the question will be current_question-1
    current_question = satisfaction_survey.questions[question_num-1].question
    current_choices = satisfaction_survey.questions[question_num-1].choices

    return render_template("questions.html", title=satisfaction_survey.title, current_question=current_question, current_choices=current_choices, question_num=question_num)


@app.route("/answer", methods=["POST"])
def answers():
    """Add answer to our responses list then redirect customer to the next question OR to a thank you page"""

    responses = session["responses"]
    responses.append(request.form.get('answer'))
    session["responses"] = responses

    # current_question_num will be a string, we need to convert to an int to add, then convert back to string for the path
    current_question = int(request.form.get('current_question_num'))

    if current_question >= len(satisfaction_survey.questions):
        return redirect("/thankyou")
    
    next_question = str(current_question + 1)
        
    next_path = f"/questions/{next_question}"
    
    return redirect(next_path)


@app.route("/thankyou")
def thank_you():
    return render_template("thankyou.html")