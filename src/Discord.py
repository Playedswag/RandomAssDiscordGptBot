
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
from DataSave import save_message



from gpt import should_reply, GetInput

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

print(f"Token loaded!")

Debug_Handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Frank Ocean"))


@bot.event
async def on_message(message):
    print(f"[DEBUG] Message from {message.author}: {message.content}")

    if message.author == bot.user:
        return

    formatted_message = f"{message.author.display_name} says: {message.content}"
    
    save_message("user", formatted_message)
    if await should_reply(message.content):
        async with message.channel.typing():
            await asyncio.sleep(2)
            response = await GetInput(formatted_message)
        await message.channel.send(response)

bot.run(token, log_handler=Debug_Handler, log_level=logging.DEBUG)