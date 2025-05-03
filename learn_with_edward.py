import json
import random
from datetime import datetime
from typing import Dict, List, Optional

class User:
    def __init__(self, username: str, password: str, age: int, school_grade: int, native_language: str = "italian"):
        self.username = username
        self.password = password  # In production, use proper password hashing
        self.age = age
        self.school_grade = school_grade
        self.native_language = native_language
        self.subscription_level = "free"  # free, premium
        self.badges = []
        self.xp = 0
        self.learning_progress = {}
        self.last_login = datetime.now()
        
    def update_subscription(self, new_level: str):
        valid_levels = ["free", "premium"]
        if new_level.lower() in valid_levels:
            self.subscription_level = new_level.lower()
            return True
        return False
    
    def add_badge(self, badge_name: str):
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            return True
        return False
    
    def add_xp(self, amount: int):
        self.xp += amount
        # Check for level up based on XP
        return self.xp
    
    def update_progress(self, topic: str, score: float):
        self.learning_progress[topic] = score
        return True
    
    def to_dict(self):
        return {
            "username": self.username,
            "age": self.age,
            "school_grade": self.school_grade,
            "native_language": self.native_language,
            "subscription_level": self.subscription_level,
            "badges": self.badges,
            "xp": self.xp,
            "learning_progress": self.learning_progress,
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S")
        }

class Quiz:
    def __init__(self, quiz_id: int, title: str, questions: List[Dict], difficulty: str, 
                 language_level: str, aligned_grade: int, topic: str):
        self.quiz_id = quiz_id
        self.title = title
        self.questions = questions
        self.difficulty = difficulty  # easy, medium, hard
        self.language_level = language_level  # A1, A2, B1, B2, etc.
        self.aligned_grade = aligned_grade  # School grade this aligns with
        self.topic = topic  # Grammar, vocabulary, etc.
        
    def take_quiz(self, user: User) -> Dict:
        print(f"\nTaking quiz: {self.title} ({self.difficulty})")
        print(f"Aligned with grade {self.aligned_grade} - {self.language_level} level")
        
        score = 0
        user_answers = []
        
        for i, question in enumerate(self.questions, 1):
            print(f"\nQuestion {i}: {question['question']}")
            
            # Display options (translate if needed)
            if user.native_language == "italian" and "translations" in question:
                print(f"(Italian: {question['translations']['italian']['question']})")
                
                for idx, option in enumerate(question["options"]):
                    print(f"{idx+1}. {option} ({question['translations']['italian']['options'][idx]})")
            else:
                for idx, option in enumerate(question["options"]):
                    print(f"{idx+1}. {option}")
            
            # Get user answer
            while True:
                try:
                    answer = int(input("Your answer (1-4): ")) - 1
                    if 0 <= answer < len(question["options"]):
                        break
                    print("Invalid choice. Please enter a number between 1 and 4.")
                except ValueError:
                    print("Please enter a number.")
            
            is_correct = (answer == question["correct_answer"])
            if is_correct:
                score += 1
                print("Correct!")
            else:
                print(f"Incorrect. The correct answer was: {question['options'][question['correct_answer']]}")
            
            user_answers.append({
                "question_id": question["id"],
                "user_answer": answer,
                "is_correct": is_correct
            })
        
        total_questions = len(self.questions)
        percentage = (score / total_questions) * 100
        
        # Update user progress
        user.update_progress(self.topic, percentage)
        
        # Award XP based on performance
        xp_earned = int(percentage * 2)  # Scale as needed
        user.add_xp(xp_earned)
        
        # Check for badges
        if percentage >= 90:
            user.add_badge(f"Master of {self.topic}")
        elif percentage >= 70:
            user.add_badge(f"{self.topic} Explorer")
        
        print(f"\nQuiz completed! Score: {score}/{total_questions} ({percentage:.1f}%)")
        print(f"XP earned: {xp_earned}")
        
        return {
            "quiz_id": self.quiz_id,
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "xp_earned": xp_earned,
            "answers": user_answers,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class LearnWithEdward:
    def __init__(self):
        self.users = {}  # username: User
        self.quizzes = []  # List of Quiz objects
        self.current_user = None
        
        # Load some sample quizzes
        self._load_sample_quizzes()
    
    def _load_sample_quizzes(self):
        # Sample quizzes aligned with Italian school curriculum
        sample_quizzes = [
            {
                "quiz_id": 1,
                "title": "Basic English Greetings",
                "difficulty": "easy",
                "language_level": "A1",
                "aligned_grade": 1,
                "topic": "Greetings",
                "questions": [
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
                    },
                    {
                        "id": 102,
                        "question": "What is the response to 'Thank you'?",
                        "options": ["Goodbye", "Please", "You're welcome", "Hello"],
                        "correct_answer": 2,
                        "translations": {
                            "italian": {
                                "question": "Qual è la risposta a 'Grazie'?",
                                "options": ["Arrivederci", "Per favore", "Prego", "Ciao"]
                            }
                        }
                    }
                ]
            },
            {
                "quiz_id": 2,
                "title": "Present Simple Verbs",
                "difficulty": "medium",
                "language_level": "A2",
                "aligned_grade": 3,
                "topic": "Verbs",
                "questions": [
                    {
                        "id": 201,
                        "question": "Which sentence is correct?",
                        "options": [
                            "She go to school every day",
                            "She goes to school every day",
                            "She is go to school every day",
                            "She going to school every day"
                        ],
                        "correct_answer": 1,
                        "translations": {
                            "italian": {
                                "question": "Quale frase è corretta?",
                                "options": [
                                    "Lei andare a scuola ogni giorno",
                                    "Lei va a scuola ogni giorno",
                                    "Lei è andare a scuola ogni giorno",
                                    "Lei andando a scuola ogni giorno"
                                ]
                            }
                        }
                    }
                ]
            }
        ]
        
        for quiz_data in sample_quizzes:
            self.quizzes.append(Quiz(**quiz_data))
    
    def register_user(self):
        print("\nRegister a new account")
        username = input("Username: ")
        
        if username in self.users:
            print("Username already exists.")
            return False
        
        password = input("Password: ")
        age = int(input("Age: "))
        grade = int(input("School grade (1-12): "))
        
        new_user = User(username, password, age, grade)
        self.users[username] = new_user
        print("Registration successful!")
        return True
    
    def login(self):
        print("\nLogin")
        username = input("Username: ")
        password = input("Password: ")
        
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            self.current_user.last_login = datetime.now()
            print(f"Welcome back, {username}!")
            return True
        
        print("Invalid username or password.")
        return False
    
    def logout(self):
        if self.current_user:
            print(f"Goodbye, {self.current_user.username}!")
            self.current_user = None
            return True
        return False
    
    def recommend_quizzes(self) -> List[Quiz]:
        if not self.current_user:
            return []
        
        # Simple recommendation based on user's grade and progress
        recommended = []
        
        for quiz in self.quizzes:
            # Check if quiz is appropriate for user's grade (±1 grade)
            if abs(quiz.aligned_grade - self.current_user.school_grade) <= 1:
                # Check if user hasn't mastered this topic yet
                if quiz.topic not in self.current_user.learning_progress or \
                   self.current_user.learning_progress[quiz.topic] < 80:
                    recommended.append(quiz)
        
        return recommended
    
    def take_quiz(self, quiz_id: int):
        if not self.current_user:
            print("Please login first.")
            return False
        
        quiz = next((q for q in self.quizzes if q.quiz_id == quiz_id), None)
        if not quiz:
            print("Quiz not found.")
            return False
        
        # Check subscription level for premium content
        if quiz.difficulty == "hard" and self.current_user.subscription_level != "premium":
            print("This quiz requires a premium subscription.")
            return False
        
        result = quiz.take_quiz(self.current_user)
        return True
    
    def view_profile(self):
        if not self.current_user:
            print("Please login first.")
            return False
        
        user_data = self.current_user.to_dict()
        print("\nUser Profile")
        print(f"Username: {user_data['username']}")
        print(f"Age: {user_data['age']}")
        print(f"School Grade: {user_data['school_grade']}")
        print(f"Subscription: {user_data['subscription_level'].capitalize()}")
        print(f"Total XP: {user_data['xp']}")
        
        print("\nBadges Earned:")
        for badge in user_data['badges']:
            print(f"- {badge}")
        
        print("\nLearning Progress:")
        for topic, score in user_data['learning_progress'].items():
            print(f"- {topic}: {score:.1f}%")
        
        return True
    
    def upgrade_subscription(self):
        if not self.current_user:
            print("Please login first.")
            return False
        
        if self.current_user.subscription_level == "premium":
            print("You already have a premium subscription.")
            return False
        
        print("\nUpgrade to Premium Subscription")
        print("Benefits:")
        print("- Access to all quizzes including advanced content")
        print("- Additional learning materials")
        print("- Progress reports")
        print(f"Price: €9.99/month")
        
        confirm = input("Would you like to upgrade? (yes/no): ").lower()
        if confirm == "yes":
            self.current_user.update_subscription("premium")
            print("Upgrade successful! Thank you for subscribing.")
            return True
        
        print("Upgrade cancelled.")
        return False

def main():
    app = LearnWithEdward()
    
    while True:
        print("\n=== Learn with Edward ===")
        if app.current_user:
            print(f"Logged in as: {app.current_user.username} (XP: {app.current_user.xp})")
            print("1. Take a Quiz")
            print("2. View Recommended Quizzes")
            print("3. View Profile")
            print("4. Upgrade Subscription")
            print("5. Logout")
        else:
            print("1. Login")
            print("2. Register")
            print("3. Exit")
        
        choice = input("Select an option: ")
        
        try:
            if app.current_user:
                if choice == "1":
                    # Show available quizzes
                    print("\nAvailable Quizzes:")
                    for quiz in app.quizzes:
                        sub_req = "(Premium)" if quiz.difficulty == "hard" else ""
                        print(f"{quiz.quiz_id}. {quiz.title} - {quiz.difficulty} {sub_req}")
                    
                    quiz_id = int(input("Enter quiz ID to take: "))
                    app.take_quiz(quiz_id)
                
                elif choice == "2":
                    recommended = app.recommend_quizzes()
                    print("\nRecommended Quizzes:")
                    if not recommended:
                        print("No recommendations available. You may have mastered all quizzes for your level!")
                    else:
                        for quiz in recommended:
                            print(f"{quiz.quiz_id}. {quiz.title} - {quiz.topic} (Grade {quiz.aligned_grade}, {quiz.language_level})")
                
                elif choice == "3":
                    app.view_profile()
                
                elif choice == "4":
                    app.upgrade_subscription()
                
                elif choice == "5":
                    app.logout()
                
                else:
                    print("Invalid choice.")
            
            else:
                if choice == "1":
                    app.login()
                
                elif choice == "2":
                    app.register_user()
                
                elif choice == "3":
                    print("Goodbye!")
                    break
                
                else:
                    print("Invalid choice.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
