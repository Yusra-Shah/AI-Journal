from groq import Groq
import streamlit as st

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def get_ai_response(user_message, mood):
    prompt = f"""
    You are a compassionate AI journal companion called Matcha.
    The user is feeling {mood} today.
    Respond with empathy and warmth in 2-4 sentences.
    End with one gentle follow-up question.
    Never give medical advice. Keep your tone soft and grounding.

    User said: {user_message}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content