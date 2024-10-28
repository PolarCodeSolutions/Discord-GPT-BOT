import discord
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace these with your actual Discord bot token and OpenAI API key
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

# Set up the bot with Discord's intents
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def split_message(message, max_length=2000):
    """Split a message into chunks of max_length."""
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Avoid the bot responding to itself or other bots
    if message.author == bot.user or message.author.bot:
        return

    # Check if the message starts with the prefix to activate the bot
    if message.content.startswith('!ask'):
        question = message.content[len('!ask '):]  # Get the question text after the prefix
        await message.channel.send("Thinking... 🤔")

        try:
            # Send the question to OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ]
            )

            answer = response['choices'][0]['message']['content']

            # Split the answer if it's too long
            for part in split_message(answer):
                await message.channel.send(part)
        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("Sorry, something went wrong.")

    if message.content.startswith('!help'):
        await message.channel.send("Ask me anything! Just type `!ask` followed by your question.")

    if message.content.startswith('!test'):
        await message.channel.send("Test ok! 🎉")

        


# Run the bot
bot.run(DISCORD_TOKEN)
