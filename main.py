import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import game

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f"{bot.user.name} is ready and deployed!")

@bot.hybrid_command()
async def play(ctx):
  embed_color = 0x330066
  one = '1️⃣'
  two = '2️⃣'
  three = '3️⃣'
  valid_reactions = ['1️⃣', '2️⃣', '3️⃣']

  max_round = 0
  
  embed = discord.Embed(title='Menu', description=f'{one} - Guess the Novel\'s Country 1 Round\n{two} - Guess the Novel\'s Country 5 Rounds\n{three} - Guess the Novel\'s Country 10 Rounds\n', color=embed_color)
  msg = await ctx.channel.send(embed=embed)
  await msg.add_reaction(one)
  await msg.add_reaction(two)
  await msg.add_reaction(three)

  def check(reaction, user):
    return user == ctx.author and str(reaction.emoji) in valid_reactions
  
  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
  except asyncio.TimeoutError:
    print("Timeout Error")
  else:
    if str(reaction.emoji) == one:
      max_round = 1
    elif str(reaction.emoji) == two:
      max_round = 5
    elif str(reaction.emoji) == three:
      max_round = 10
    await game.play_game(bot, ctx, embed, msg, max_round)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
