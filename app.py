from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, surveys

app = Flask(__name__)

app.config["SECRET_KEY"] = "123"
debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    return render_template("home.html", surveys=surveys)

@app.route("/", methods=["post"])
def survey_selection():
    survey = request.form["selected_survey"]
    return redirect(f"/survey/{survey}")

@app.route("/survey/<survey>")
def survey_title(survey):
    return render_template("survey_title.html", title=surveys[survey].title, instructions=surveys[survey].instructions, survey=survey)

@app.route("/questions/<survey>/<int:question_num>")
def questions_page(survey, question_num):
    responses_loc = f"{survey}_responses"
    responses = session.get(responses_loc, [])
    if len(responses) == len(surveys[survey].questions):
        return redirect(f"/thankyou/{survey}")
    if question_num != len(responses):
        flash("Invalid URL!")
        return redirect(f"/questions/{survey}/{len(responses)}")
    question = surveys[survey].questions[question_num]
    return render_template("question.html", question=question, num=question_num)

@app.route("/questions/<survey>/<int:question_num>", methods=["post"])
def save_answer(survey,question_num):
    answer = request.form
    responses_loc = f"{survey}_responses"
    responses = session.get(responses_loc,[])
    responses.append(answer["choices"])
    session[responses_loc] = responses
    return redirect(f"/questions/{survey}/{str(question_num + 1)}")
    
@app.route("/thankyou/<survey>")
def thank_you(survey):
    responses_loc = f"{survey}_responses"
    return render_template("thank_you.html", survey=surveys[survey], responses_loc=responses_loc, range=range(len(surveys[survey].questions)))