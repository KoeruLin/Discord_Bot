import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import llm

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user.name} is online")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        try:
            response = await asyncio.wait_for(llm.api_call(message),
                                       timeout=60)
            await message.channel.send(f"<@{message.author.id}> {response}")
        except asyncio.TimeoutError:
            await message.channel.send("bro the AI server is taking a nap 💀")

    await bot.process_commands(message)

@app_commands.describe(words="Mia is listening")
@app_commands.allowed_installs(guilds=True, users=True)  # Installs to servers and/or user profiles
@app_commands.allowed_contexts(dms=True, private_channels=True)  # Works in GDMs!
@bot.tree.command(name="advice",description="Get completely unhinged dating advice from Mi")
async def advice(interaction: discord.Interaction, words: str):
    await interaction.response.defer()
    try:
        response = await asyncio.wait_for(llm.api_call(words), timeout=60)
        await interaction.followup.send(f"Question: {words} \n <@{interaction.user.id}> {response}")
    except asyncio.TimeoutError:
        await interaction.followup.send("bro the AI server is taking a nap")

bot.run(token, log_level=logging.DEBUG)
