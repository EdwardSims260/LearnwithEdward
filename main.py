from fastapi import FastAPI
import openai
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI()
openai.api_key = "your-openai-key"

# Firebase setup
cred = credentials.Certificate("path-to-firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.post("/generate-quiz")
async def generate_quiz(subject: str, grade: int):
    prompt = f"Generate a {grade}-grade Italian curriculum {subject} quiz in JSON format..."
    response = openai.ChatCompletion.create(model="gpt-4", messages=[...])
    return response.choices[0].message.content
