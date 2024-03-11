import openai
import os
from dotenv import load_dotenv

from session import Session, SessionManager

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

session_manager = SessionManager()

def chat(session_id, prompt):
    session_manager.create_session(session_id)
    session = session_manager.get_session(session_id)
    session.add_message("user", prompt)
    
    messages = session.messages[:]  # Copy existing messages
    
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    session.add_message("system", res.choices[0].message.content.strip())

    return res.choices[0].message.content.strip()