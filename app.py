import streamlit as st
from datetime import datetime
import json
import random

# --- User & Quiz Classes (Same as before) ---
class User:
    def __init__(self, username: str, password: str, age: int, school_grade: int, native_language: str = "italian"):
        self.username = username
        self.password = password
        self.age = age
        self.school_grade = school_grade
        self.native_language = native_language
        self.subscription_level = "free"
        self.badges = []
        self.xp = 0
        self.learning_progress = {}
        self.last_login = datetime.now()

    # ... (Keep all methods from the original class)

class Quiz:
    def __init__(self, quiz_id: int, title: str, questions: list, difficulty: str, language_level: str, aligned_grade: int, topic: str):
        self.quiz_id = quiz_id
        self.title = title
        self.questions = questions
        self.difficulty = difficulty
        self.language_level = language_level
        self.aligned_grade = aligned_grade
        self.topic = topic

    def take_quiz(self, user):
        st.write(f"## {self.title} ({self.difficulty})")
        st.write(f"*Aligned with grade {self.aligned_grade} - {self.language_level} level*")

        score = 0
        user_answers = []

        for i, question in enumerate(self.questions, 1):
            st.write(f"**Question {i}:** {question['question']}")

            if user.native_language == "italian" and "translations" in question:
                st.write(f"*(Italian: {question['translations']['italian']['question']})*")

            options = question["options"]
            user_answer = st.radio(
                "Select your answer:",
                options,
                key=f"quiz_{self.quiz_id}_q_{i}"
            )

            if st.button("Submit Answer", key=f"submit_{self.quiz_id}_{i}"):
                is_correct = (options.index(user_answer) == question["correct_answer"])
                if is_correct:
                    score += 1
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. The correct answer was: {options[question['correct_answer']]}")

                user_answers.append({
                    "question_id": question["id"],
                    "user_answer": options.index(user_answer),
                    "is_correct": is_correct
                })

        total_questions = len(self.questions)
        percentage = (score / total_questions) * 100

        user.update_progress(self.topic, percentage)
        xp_earned = int(percentage * 2)
        user.add_xp(xp_earned)

        if percentage >= 90:
            user.add_badge(f"Master of {self.topic}")
        elif percentage >= 70:
            user.add_badge(f"{self.topic} Explorer")

        st.balloons()
        st.write(f"### Quiz Completed! 🎉")
        st.write(f"**Score:** {score}/{total_questions} ({percentage:.1f}%)")
        st.write(f"**XP Earned:** {xp_earned}")

        return {
            "quiz_id": self.quiz_id,
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "xp_earned": xp_earned,
            "answers": user_answers,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# --- Streamlit App ---
def main():
    st.title("Learn with Edward 🇬🇧➡️🇮🇹")
    st.markdown("An interactive English learning platform for Italian students.")

    if "users" not in st.session_state:
        st.session_state.users = {}
    if "current_user" not in st.session_state:
        st.session_state.current_user = None

    menu = ["Home", "Login", "Register", "Take Quiz", "Profile", "Upgrade"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to Learn with Edward!")
        st.write("Please login or register to start learning.")

    elif choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username].password == password:
                st.session_state.current_user = st.session_state.users[username]
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Invalid username or password.")

    elif choice == "Register":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        age = st.number_input("Age", min_value=6, max_value=18)
        grade = st.number_input("School Grade (1-12)", min_value=1, max_value=12)
        if st.button("Register"):
            if username in st.session_state.users:
                st.error("Username already exists.")
            else:
                new_user = User(username, password, age, grade)
                st.session_state.users[username] = new_user
                st.session_state.current_user = new_user
                st.success("Registration successful!")

    elif choice == "Take Quiz":
        if st.session_state.current_user:
            quiz = Quiz(
                quiz_id=1,
                title="Basic English Greetings",
                questions=[
                    {
                        "id": 101,
                        "question": "How do you say 'Hello' in the morning?",
                        "options": ["Good morning", "Good night", "Good afternoon", "Hello"],
                        "correct_answer": 0,
                        "translations": {
                            "italian": {
                                "question": "Come si dice 'Ciao' al mattino?",
                                "options": ["Buongiorno", "Buonanotte", "Buon pomeriggio", "Ciao"]
                            }
                        }
                    }
                ],
                difficulty="easy",
                language_level="A1",
                aligned_grade=1,
                topic="Greetings"
            )
            quiz.take_quiz(st.session_state.current_user)
        else:
            st.warning("Please login first.")

    elif choice == "Profile":
        if st.session_state.current_user:
            st.write("### Your Profile")
            st.write(f"**Username:** {st.session_state.current_user.username}")
            st.write(f"**XP:** {st.session_state.current_user.xp}")
            st.write("**Badges:**")
            for badge in st.session_state.current_user.badges:
                st.write(f"- {badge}")
        else:
            st.warning("Please login first.")

    elif choice == "Upgrade":
        if st.session_state.current_user:
            if st.session_state.current_user.subscription_level == "premium":
                st.info("You already have a premium subscription.")
            else:
                st.write("Upgrade to Premium for €9.99/month")
                if st.button("Upgrade Now"):
                    st.session_state.current_user.update_subscription("premium")
                    st.success("Upgraded to Premium! 🎉")
        else:
            st.warning("Please login first.")

if __name__ == "__main__":
    main()
