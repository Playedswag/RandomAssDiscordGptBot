import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASAVE_FILE = os.path.join(BASE_DIR, "Data", "ChatHistory.json")


Remembering_Messages = 5 #Change to affect the amount of messages Darius can remember, effects token usage!


def load_history():
    if not os.path.exists(DATASAVE_FILE):
        return []
    with open(DATASAVE_FILE, "r") as file:
        data = json.load(file)
        return data

def save_message(role, content):
    history = load_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "role": role,
        "content": content
    })
    with open(DATASAVE_FILE, "w") as file:
        json.dump(history, file, indent=2)

def load_chats():
    History = load_history()
    sorted_data = sorted(History, key=lambda x: datetime.fromisoformat(x['timestamp']), reverse=True)
    newest_five = sorted_data[:Remembering_Messages]
    ChatHistory = json.dumps(newest_five)
    return ChatHistory
