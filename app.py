from flask import Flask, render_template, request
import random
from questions import hr_questions, technical_questions, coding_questions

app = Flask(__name__)

SESSION_LOGS = []

def evaluate_answer(answer):
    keywords = ["project", "skills", "experience", "learning", "team"]
    score = sum(2 for k in keywords if k in answer.lower())

    if len(answer.split()) < 20:
        feedback = "Answer is too short. Explain more clearly."
    elif score >= 6:
        feedback = "Good answer. Well explained."
    else:
        feedback = "Average answer. Add examples."

    return min(score, 10), feedback


def evaluate_code(answer, keywords):
    score = sum(3 for k in keywords if k in answer)
    feedback = "Correct logic." if score >= 6 else "Improve logic."
    return min(score, 10), feedback


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    coding = None

    round_type = random.choice(["HR", "TECH", "CODE"])

    if round_type == "HR":
        question = random.choice(hr_questions)
    elif round_type == "TECH":
        question = random.choice(technical_questions)
    else:
        coding = random.choice(coding_questions)
        question = coding["question"]

    if request.method == "POST":
        answer = request.form["answer"]

        if round_type == "CODE":
            score, feedback = evaluate_code(answer, coding["keywords"])
        else:
            score, feedback = evaluate_answer(answer)

        result = {
            "type": round_type,
            "score": score,
            "feedback": feedback
        }

    return render_template("index.html", question=question, result=result)


@app.route("/save-log", methods=["POST"])
def save_log():
    SESSION_LOGS.append(request.form.get("log"))
    return "Saved"


@app.route("/admin")
def admin():
    return render_template("admin.html", logs=SESSION_LOGS)

@app.route("/completed", methods=["POST"])
def completed():
    return render_template("completed.html")



if __name__ == "__main__":
    app.run(debug=True)
