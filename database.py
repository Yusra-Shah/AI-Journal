from pymongo import MongoClient
from datetime import datetime
import streamlit as st

def get_db():
    client = MongoClient(st.secrets["MONGO_URI"])
    return client["ai_journal"]["entries"]

def save_entry(user_id, message, ai_response, mood):
    db = get_db()
    db.insert_one({
        "user_id": user_id,
        "message": message,
        "ai_response": ai_response,
        "mood": mood,
        "timestamp": datetime.now()
    })

def get_entries(user_id):
    db = get_db()
    return list(db.find({"user_id": user_id}).sort("timestamp", -1).limit(10))

def get_entry_count(user_id):
    db = get_db()
    return db.count_documents({"user_id": user_id})

def get_mood_history(user_id):
    db = get_db()
    entries = list(db.find({"user_id": user_id}, {"mood": 1}).sort("timestamp", -1).limit(30))
    return [e["mood"] for e in entries if "mood" in e]