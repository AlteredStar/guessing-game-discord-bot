#jyukyu - 쮸뀨미 jiwoo & kyujin
import gspread
import random
import asyncio

gc = gspread.service_account(filename='./guess-the-novel-434985dafe63.json')
sh = gc.open_by_key('15UVeti8zd2mlboxJrgh4GdgmhyRixxgSRM0acGBG_mQ')
curr_sheet = sh.get_worksheet(0)

def generate():
  col = random.randint(1, 2) #1 = Kyujin, 2 = Jiwoo
  return (curr_sheet.col_values(col)[random.randint(1, len(curr_sheet.col_values(col)) - 1)], col) #(img link, person)

def guess(actual, guess):
  return actual == guess

class IDOL:
  KYUJIN = 1
  JIWOO = 2

async def play_game(bot, ctx, embed, msg):
  kyujin = '🇰'
  jiwoo = '🇯'

  valid_idols = ['🇰', '🇯']
  
  await msg.clear_reactions()
  current_idol = generate()
  
  embed.description = ''
  embed.set_image(url=current_idol[0])
  embed.color = 0x330066
  await msg.edit(embed=embed)
  await msg.add_reaction(kyujin)
  await msg.add_reaction(jiwoo)

  def check(reaction, user):
    return user == ctx.author and str(reaction.emoji) in valid_idols

  try:
    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
  except asyncio.TimeoutError:
    print("Timeout Error")
  else:
    if str(reaction.emoji) == kyujin:
      guess_country = IDOL.KYUJIN
    elif str(reaction.emoji) == jiwoo:
      guess_country = IDOL.JIWOO
    game_status = guess(current_idol[1], guess_country)
  
  await msg.clear_reactions()

  if game_status:
    embed.description = "\n\n:white_check_mark: **CORRECT** :white_check_mark:\n\n"
  else:
    embed.description = "\n\n:x: **WRONG** :x:\n\n"
  
  if current_idol[1] == IDOL.KYUJIN:
      embed.description += "It was Kyujin!"
      embed.color = 0xffc0cb
  elif current_idol[1] == IDOL.JIWOO:
    embed.description += "It was Jiwoo!"
    embed.color = 0xff0000
  
  await msg.edit(embed=embed)
