import openai

from session import Session, SessionManager

openai.api_key = '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'

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