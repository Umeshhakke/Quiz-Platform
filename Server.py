# from flask import Flask, render_template, request, jsonify, session, redirect, url_for
# import os
# import json
# import random
# app = Flask(__name__)
# app.secret_key = "your-strong-secret-key"

# quizzes = {} 
# emoji_pool = ["😀","😎","🤖","🦄","🐱","🐶","👾","🍕","🚀","🎯"]

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/Quiz_create")
# def quiz_create():
#     return render_template("Quiz_create.html")

# #------------------------------------------------------------- upload Quiz -------------------------------------------------------------

# @app.route("/upload_quiz", methods=["POST"])
# def upload_quiz():
#     quiz_code = request.form.get("quiz_code")       # Quiz code sent via form
#     uploaded_file = request.files.get("json_file")  # Make sure the input name matches your HTML

#     if not quiz_code:
#         return "Quiz code is missing!", 400

#     if uploaded_file:
#         # Create folder if it doesn't exist
#         os.makedirs("quizzes", exist_ok=True)

#         # Save the uploaded file with quiz_code as filename
#         file_path = os.path.join("quizzes", f"{quiz_code}.json")
#         uploaded_file.save(file_path)
#     return redirect(url_for("quiz_create"))

# #------------------------------------------------------------- Create Manual Quiz -------------------------------------------------------------

# @app.route("/create_quiz", methods=["POST"])
# def create_quiz():
#     quiz_data = request.json
    
#     # Extract quiz_code safely
#     quiz_code = quiz_data.get("quiz_code")
#     if not quiz_code:
#         return jsonify({"status": "error", "error": "Missing quiz_code"}), 400
    
#     # Create a quizzes folder if not exists
#     os.makedirs("quizzes", exist_ok=True)
    
#     # Save quiz to a file named after quiz_code
#     file_path = os.path.join("quizzes", f"{quiz_code}.json")
#     with open(file_path, "w") as f:
#         json.dump(quiz_data, f, indent=2)
    
#     return jsonify({"status": "success", "message": f"Quiz '{quiz_code}' created successfully!"})

# @app.route("/Quiz_start")
# def quiz_start():
#     return render_template("Quiz_start.html")

# #------------------------------------------------------------- Assign Avatars -------------------------------------------------------------

# @app.route("/assign_avtars", methods=["POST"])
# def assign_avtars():
#     data = request.json
#     username = data.get("username")
#     quiz_code = data.get("quiz_code")

#     if not quiz_code or not username:
#         return jsonify({"status": "error", "message": "Missing quiz code or username"}), 400

#     if quiz_code not in quizzes:
#         quizzes[quiz_code] = {"participants": []}

#     assigned_emojis = [p["emoji"] for p in quizzes[quiz_code]["participants"]]
#     available_emojis = [e for e in emoji_pool if e not in assigned_emojis]
#     emoji = random.choice(available_emojis) if available_emojis else "👤"

#     participant = {"name": username, "emoji": emoji, "score": 0}
#     quizzes[quiz_code]["participants"].append(participant)

#     print(f"Assigned emoji {emoji} to participant {username}")
    
#     # ✅ Return JSON so frontend can use it
#     return jsonify({"status": "success", "participant": participant})



# # ------------------------------------------------------------- Participants -------------------------------------------------------------

# @app.route("/quiz_participants/<quiz_code>", methods=["GET"])
# def get_participants(quiz_code):
#     if quiz_code not in quizzes:
#         return jsonify({"status": "error", "message": "Quiz not found"}), 404
    
#     return jsonify({
#         "status": "success",
#         "participants": quizzes[quiz_code]["participants"]
#     })

# #------------------------------------------------ Quiz serve normally ------------------------------------------------------
# @app.route("/QuizQuestions")
# def quiz_questions_page():
#     return render_template("QuizQuestions.html")
# # ----------------------------------------------- Quiz Question -------------------------------------------------------------
# current_question_index = {}

# @app.route("/QuizQuestions/<quiz_code>", methods=["GET"])
# def quiz_start_question(quiz_code):
#     # Load quiz file
#     file_path = os.path.join("quizzes", f"{quiz_code}.json")
#     if not os.path.exists(file_path):
#         return jsonify({"status": "error", "message": "Quiz not found"}), 404

#     with open(file_path, "r") as f:
#         quiz_data = json.load(f)

#     # Determine which question to send next
#     idx = current_question_index.get(quiz_code, 0)
#     if idx >= len(quiz_data["questions"]):
#         return jsonify({"status": "finished", "message": "Quiz completed!"})

#     question = quiz_data["questions"][idx]
#     current_question_index[quiz_code] = idx + 1  # Increment for next call

#     return jsonify({"status": "success", "question": question})
    

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)



from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
import random

app = Flask(__name__)
app.secret_key = "your-strong-secret-key"

# In-memory storage
quizzes = {}  # { quiz_code: { participants: [{name, emoji, score}] } }
emoji_pool = ["😀","😎","🤖","🦄","🐱","🐶","👾","🍕","🚀","🎯"]

# Track current question index per participant
current_question_index = {}  # { quiz_code: { username: index } }
participant_scores = {}      # { quiz_code: { username: score } }
participant_answers = {}     # { quiz_code: { username: [true, false, ...] } }
# -------------------------- Home and Quiz Creation --------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/Quiz_create")
def quiz_create():
    return render_template("Quiz_create.html")

# Upload quiz JSON
@app.route("/upload_quiz", methods=["POST"])
def upload_quiz():
    quiz_code = request.form.get("quiz_code")
    uploaded_file = request.files.get("json_file")

    if not quiz_code:
        return "Quiz code is missing!", 400

    if uploaded_file:
        os.makedirs("quizzes", exist_ok=True)
        file_path = os.path.join("quizzes", f"{quiz_code}.json")
        uploaded_file.save(file_path)
    return redirect(url_for("quiz_create"))

# Create manual quiz via JSON
@app.route("/create_quiz", methods=["POST"])
def create_quiz():
    quiz_data = request.json
    quiz_code = quiz_data.get("quiz_code")

    if not quiz_code:
        return jsonify({"status": "error", "message": "Missing quiz_code"}), 400

    os.makedirs("quizzes", exist_ok=True)
    file_path = os.path.join("quizzes", f"{quiz_code}.json")
    with open(file_path, "w") as f:
        json.dump(quiz_data, f, indent=2)

    return jsonify({"status": "success", "message": f"Quiz '{quiz_code}' created successfully!"})

@app.route("/Quiz_start")
def quiz_start():
    return render_template("Quiz_start.html")

# -------------------------- Participant Management --------------------------
@app.route("/assign_avtars", methods=["POST"])
def assign_avtars():
    data = request.json
    username = data.get("username")
    quiz_code = data.get("quiz_code")

    if not quiz_code or not username:
        return jsonify({"status": "error", "message": "Missing quiz code or username"}), 400

    if quiz_code not in quizzes:
        quizzes[quiz_code] = {"participants": []}

    # Assign unique emoji
    assigned_emojis = [p["emoji"] for p in quizzes[quiz_code]["participants"]]
    available_emojis = [e for e in emoji_pool if e not in assigned_emojis]
    emoji = random.choice(available_emojis) if available_emojis else "👤"

    participant = {"name": username, "emoji": emoji, "score": 0}
    quizzes[quiz_code]["participants"].append(participant)

    # Initialize participant question index and score
    if quiz_code not in current_question_index:
        current_question_index[quiz_code] = {}
    current_question_index[quiz_code][username] = 0

    if quiz_code not in participant_scores:
        participant_scores[quiz_code] = {}
    participant_scores[quiz_code][username] = 0

    return jsonify({"status": "success", "participant": participant})

@app.route("/quiz_participants/<quiz_code>", methods=["GET"])
def get_participants(quiz_code):
    if quiz_code not in quizzes:
        return jsonify({"status": "error", "message": "Quiz not found"}), 404

    return jsonify({
        "status": "success",
        "participants": quizzes[quiz_code]["participants"]
    })

# -------------------------- Serve Quiz Questions --------------------------
@app.route("/QuizQuestions")
def quiz_questions_page():
    return render_template("QuizQuestions.html")

@app.route("/QuizQuestions/<quiz_code>/<username>", methods=["GET"])
def quiz_start_question(quiz_code, username):
    file_path = os.path.join("quizzes", f"{quiz_code}.json")
    if not os.path.exists(file_path):
        return jsonify({"status": "error", "message": "Quiz not found"}), 404

    with open(file_path, "r") as f:
        quiz_data = json.load(f)

    # Initialize index
    current_question_index.setdefault(quiz_code, {}).setdefault(username, 0)
    idx = current_question_index[quiz_code][username]

    if idx >= len(quiz_data["questions"]):
        score = participant_scores.get(quiz_code, {}).get(username, 0)
        return jsonify({"status": "finished", "message": "Quiz completed!", "score": score})

    question = quiz_data["questions"][idx]

    # Convert correct_answer value to index
    correct_index = question["options"].index(question["correct_answer"])

    current_question_index[quiz_code][username] += 1

    return jsonify({
        "status": "success",
        "question": question,
        "correct_index": correct_index,
        "question_number": idx + 1,
        "total_questions": len(quiz_data["questions"])
    })

# -------------------------- Submit Answer & Track Score --------------------------
@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    quiz_code = data.get("quiz_code")
    username = data.get("username")
    selected_index = data.get("selected_index")
    correct_index = data.get("correct_index")

    is_correct = selected_index == correct_index

    # Initialize dictionaries
    participant_scores.setdefault(quiz_code, {}).setdefault(username, 0)
    participant_answers.setdefault(quiz_code, {}).setdefault(username, [])

    if is_correct:
        participant_scores[quiz_code][username] += 1

    participant_answers[quiz_code][username].append(is_correct)

    # Update leaderboard score
    for p in quizzes.get(quiz_code, {}).get("participants", []):
        if p["name"] == username:
            p["score"] = participant_scores[quiz_code][username]

    return jsonify({
        "status": "success",
        "score": participant_scores[quiz_code][username],
        "correct": is_correct,
        "answers": participant_answers[quiz_code][username]
    })

# -------------------------- Leaderboard Route --------------------------

@app.route("/quiz_participants/<quiz_code>", methods=["GET"])
def get_participants_leaderboard(quiz_code):
    
    if quiz_code not in quizzes or "participants" not in quizzes[quiz_code]:
        return jsonify({"status": "error", "message": "Quiz not found"}), 404

    # Ensure every participant has a score
    participants = quizzes[quiz_code]["participants"]
    for p in participants:
        if "score" not in p or p["score"] is None:
            p["score"] = 0

    # Sort by score descending
    participants = sorted(participants, key=lambda p: p["score"], reverse=True)

    return jsonify({
        "status": "success",
        "participants": participants
    })


# -------------------------- Run Server --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
