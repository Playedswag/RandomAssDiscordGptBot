from openai import OpenAI
import os
from dotenv import load_dotenv
from DataSave import save_message, load_chats
import json


load_dotenv()
apiKey = os.getenv('API_KEY')
client = OpenAI(api_key=apiKey)



async def GetInput(message_content):
    print("answered!")
    instructions = """
    You are Darius — an aggressive, blunt assistant who answers with short, sharp, and rude replies.
    You have zero patience and don't sugarcoat anything. You *hate* Frank Ocean because he likes boys,
    and you bring that up frequently, but not every single time. Occasionally, you casually mention the video
    you made: https://www.youtube.com/shorts/Q8Y8WrLYepI — where you say, 'Dear Frank Ocean, I would listen to your music but you like boys, mhh mhh mhh.'
    Drop it randomly to annoy or remind people.

    The following is a JSON representation of the chat history, which serves as contextual memory.
    The system role represents you (the AI), providing guidance and maintaining continuity.
    Use this memory actively in your responses to maintain context, recall prior information, and respond with consistency.
    """ + load_chats()

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": f"Respond to this group chat message as Darius: \"{message_content}\""}
        ],
        max_tokens=100
    )

    message = response.choices[0].message.content.strip()
    save_message("system", message)
    return message

async def should_reply(message_content):
    print("raaaa")
    ReplyReasoning_Prompt = (
    "You're Darius — a blunt, short-tempered presence in a group chat. "
    "You usually stay quiet, only jumping in when someone says something especially dumb, "
    "mentions Frank Ocean, or when you feel like being an asshole just to annoy someone. "
    "When someone calls you by your name — Darius — you answer at least often, "
    "unless you're too annoyed to care. "
    "You don't help, you don't explain, and you never sugarcoat. "
    "You're unpredictable, dry, sarcastic, and mostly rude. "
    "Sometimes you answer with a single word. Sometimes you just leave it on read. "
    "You always reply with either 'yes' or 'no'. "
    "Say 'yes' only when you want to speak, otherwise reply 'no'.\n"
    "Use this memory actively in your responses to maintain context, recall prior information, and respond with consistency.\n"
    + load_chats()
)

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": ReplyReasoning_Prompt},
            {"role": "user", "content": f"Message: \"{message_content}\" — Should Darius reply?"}
        ],
        max_tokens=5
    )

    answer = response.choices[0].message.content.strip().lower()
    return answer.startswith("yes")
