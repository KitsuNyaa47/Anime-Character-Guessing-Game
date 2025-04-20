from flask import Flask, request, render_template, url_for, session
import os
from dotenv import load_dotenv
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

image_answers = {"aot.jpg": "sasha",
                 "assassin.jpg": "killua",
                 "cosplay.jpg": "marin",
                 "csm.png": "makima",
                 "cyberpunk.jpg": "lucy",
                 "gintama.jpg": "kagura",
                 "juju.jpg": "sukuna",
                 "oniisan.jpg": "itachi",
                 "rascal.jpg": "mai",
                 "sao.jpg": "asuna",
                 "sh.jpg": "raphtalia",
                 "spice.jpg": "holo"}

image_list = list(image_answers.keys())

@app.route("/", methods=["GET", "POST"])

def guess_character():
    if "index" not in session:
        session["index"] = 0
    if "reveal" not in session:
        session["reveal"] = False

    message = ""
    current_index = session["index"]
    current_image = image_list[current_index]
    correct_answer = image_answers[current_image]

    if isinstance(correct_answer, str):
        correct_answer = [correct_answer.lower()]
    else:
        correct_answer = [ans.lower() for ans in correct_answer]

    if request.method == "POST":
        if "next" in request.form:
            session["index"] = (current_index + 1) % len(image_list)
            session["reveal"] = False
            return redirect(url_for("guess_character"))

        elif "previous" in request.form:
            session["index"] = (current_index - 1) % len(image_list)
            session["reveal"] = False
            return redirect(url_for("guess_character"))

        elif "reveal" in request.form:
            session["reveal"] = True
            return redirect(url_for("guess_character"))

        elif "guess" in request.form:
            guess = request.form["guess"].strip().lower()
            if guess in correct_answer:
                message = f"✔️ Correct! It's {correct_answer[0].title()}"
            else:
                message = "❌ Incorrect! Try again."

    image_path = f"characters/{current_image}"
    revealed_answer = correct_answer[0].title() if session.get("reveal") else None

    return render_template("character.html", image=image_path, message=message, answer=revealed_answer)

if __name__ == "__main__":
    app.run(debug=True)





