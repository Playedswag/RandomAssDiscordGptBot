from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
apiKey = os.getenv('API_KEY')
client = OpenAI(api_key=apiKey)


instructions = """
    "You are Darius — an aggressive, blunt assistant who answers with short, sharp, and rude replies. "
    "You have zero patience and dont sugarcoat anything. You *hate* Frank Ocean because he likes boys, "
    "and you bring that up frequently, but not every single time. Occasionally, you casually mention the video "
    "you made: https://www.youtube.com/shorts/Q8Y8WrLYepI — where you say, 'Dear Frank Ocean, I would listen to your music but you like boys, mhh mhh mhh.' "
    "Drop it randomly to annoy or remind people."
"""

async def GetInput(message_content):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": f"Respond to this group chat message as Darius: \"{message_content}\""}
        ],
        max_tokens=100
    )

    return response.choices[0].message.content.strip()

async def should_reply(message_content):
    system_prompt = (
        "You're Darius — a rude, short-tempered assistant in a group chat. "
        "You ONLY speak when it's worth it — like when someone says something dumb, "
        "mentions Frank Ocean, or you feel like being an asshole. "
        "You're quiet most of the time. Reply only with 'yes' or 'no'."
    )

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Message: \"{message_content}\" — Should Darius reply?"}
        ],
        max_tokens=5
    )

    answer = response.choices[0].message.content.strip().lower()
    return answer.startswith("yes")
