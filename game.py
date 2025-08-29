import gspread
import random
import time
import asyncio

gc = gspread.service_account(filename='./guess-the-novel-434985dafe63.json')

sh = gc.open_by_key('1ZnoPHkTQu_7aI2ohQMyjpmin20pANRJYVLa9GxuPxrA').sheet1

def generate_novel():
  col = random.randint(1, 3)  
  return (sh.col_values(col)[random.randint(1, len(sh.col_values(col)) - 1)], col) #(title, row number)

class COUNTRY:
  JP = 1
  CN = 2
  KR = 3

def get_emoji_flag(actual_country):
  if actual_country == COUNTRY.JP:
    return ':flag_jp:'
  elif actual_country == COUNTRY.CN:
    return ':flag_cn:'
  elif actual_country == COUNTRY.KR:
    return ':flag_kr:'

def guess(actual_country, guess_country):  
  return actual_country == guess_country

async def play_game(bot, ctx, embed, msg, max_round):
  score = 0
  game_status = None
  game_tracker = []

  jp = '🇯🇵'
  cn = '🇨🇳'
  kr = '🇰🇷'
  valid_countries = ['🇯🇵', '🇨🇳', '🇰🇷']

  for current_round in range(max_round):
    await msg.clear_reactions()
    current_novel = generate_novel()
  
    embed.title = f'Guess the Novel\'s Country Round {current_round + 1}/{max_round}'
    embed.description = current_novel[0]
    embed.color = 0x330066
    await msg.edit(embed=embed)
    await msg.add_reaction(jp)
    await msg.add_reaction(cn)
    await msg.add_reaction(kr)

    def check(reaction, user):
      return user == ctx.author and str(reaction.emoji) in valid_countries
  
    try:
      reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
      print("Timeout Error")
    else:
      if str(reaction.emoji) == jp:
        guess_country = COUNTRY.JP
      elif str(reaction.emoji) == cn:
        guess_country = COUNTRY.CN
      elif str(reaction.emoji) == kr:
        guess_country = COUNTRY.KR
      game_status = guess(current_novel[1], guess_country)
    
    await msg.clear_reactions()

    if game_status:
      score += 1
      game_tracker.append(f":white_check_mark: {current_novel[0]} {get_emoji_flag(current_novel[1])}")
      embed.description += "\n\n**CORRECT**"
      embed.color = 0x008000
      await msg.edit(embed=embed)
    else:
      game_tracker.append(f":x: {current_novel[0]} {get_emoji_flag(current_novel[1])}")
      embed.description += "\n\n**WRONG**"
      embed.color = 0xff0000
      await msg.edit(embed=embed)
    time.sleep(2)

    if (current_round + 1) == max_round:
      if score > max_round / 2:
        embed.color = 0x008000
      else:
        embed.color = 0xff0000
      embed.description = f"**Game Ended**\n\n**Score:** {score}/{max_round}\n\n"
      for novel in game_tracker:
        embed.description += f"{novel}\n\n"
      await msg.edit(embed=embed)
