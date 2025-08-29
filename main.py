import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio
import country_game
import jyukyu_game

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

@bot.hybrid_command(aliases=['kj', 'jyukyu'])
async def jk(ctx):
  embed = discord.Embed(title='Kyujin or Jiwoo?', description='Starting...', color=0x330066)
  msg = await ctx.channel.send(embed=embed)
  await jyukyu_game.play_game(bot, ctx, embed, msg)

@bot.hybrid_command(aliases=['qpn', 'qn'])
async def qp(ctx):
  embed = discord.Embed(title='Guess The Country (Novel) Quick Play', description='Starting...', color=0x330066)
  msg = await ctx.channel.send(embed=embed)
  await country_game.play_game(bot, ctx, embed, msg, 1, 'Novel')

@bot.hybrid_command(aliases=['qg'])
async def qpg(ctx):
  embed = discord.Embed(title='Guess The Country (Gacha) Quick Play', description='Starting...', color=0x330066)
  msg = await ctx.channel.send(embed=embed)
  await country_game.play_game(bot, ctx, embed, msg, 1, 'Gacha')

@bot.hybrid_command()
async def play(ctx):
  embed_color = 0x330066
  novel = '📚'
  gacha_game = '🎮'
  valid_games = ['📚', '🎮']
  one = '1️⃣'
  two = '2️⃣'
  three = '3️⃣'
  valid_rounds = ['1️⃣', '2️⃣', '3️⃣']

  game_mode = 'default'
  max_round = 0
  
  async def display_emotes(msg, emojis):
    for emote in emojis:
      await msg.add_reaction(emote)

  menu_desc = f"""
    {novel} - Guess The Country: Novel Edition\n
    {gacha_game} - Guess The Country: Gacha Game Edition
  """
  embed = discord.Embed(title='Menu', description=menu_desc, color=embed_color)
  msg = await ctx.channel.send(embed=embed)
  await display_emotes(msg, valid_games)

  #check for game mode selection
  def check_game(reaction, user):
    return user == ctx.author and str(reaction.emoji) in valid_games
  
  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_game)
  except asyncio.TimeoutError:
    print("Timeout Error")
  else:
    if str(reaction.emoji) == novel:
      game_mode = 'Novel'
    elif str(reaction.emoji) == gacha_game:
      game_mode = 'Gacha'

  await msg.clear_reactions()

  embed.title += f" - Guess The Country ({game_mode})"
  round_desc = f"""
    {one} - 5 Rounds\n
    {two} - 10 Rounds\n
    {three} - 15 Rounds\n
  """
  embed.description = round_desc
  await msg.edit(embed=embed)
  await display_emotes(msg, valid_rounds)

  #check for how many rounds
  def check_round(reaction, user):
    return user == ctx.author and str(reaction.emoji) in valid_rounds
  
  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_round)
  except asyncio.TimeoutError:
    print("Timeout Error")
  else:
    if str(reaction.emoji) == one:
      max_round = 5
    elif str(reaction.emoji) == two:
      max_round = 10
    elif str(reaction.emoji) == three:
      max_round = 15
    await country_game.play_game(bot, ctx, embed, msg, max_round, game_mode)

@bot.command()
async def h(ctx):
  desc = """
    **General Commands:**
    !play - Opens the game menu for Guess The Country
    !help, !h - Opens help menu
    !jk, !kj, !jyukyu - Play a single round of Kyujin or Jiwoo?
    \n
    **Quick Play Commands:**
    !qp, !qpn !qn - Play a single round of Guess The Country (Novel)
    !qpg, !qg - Play a single round of Guess The Country (Gacha)
  """
  embed = discord.Embed(title='Help Menu', description=desc, color=0x330066)
  await ctx.channel.send(embed=embed)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
