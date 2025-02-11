# ========================================= IMPORTS ========================================= #

# to install discord library: <python3 -m pip install -U discord.py>
import discord
from discord.ext import commands
from discord import app_commands
# to install dotenv library: <pip install python-dotenv>
from dotenv import load_dotenv
from guild_config import TEST_GUILD_ID
import json
import os
import random
import pyquotegen
import requests
# imports from other files

# ============================================================================================== #
# ====================================== DISCORD BOT INIT ======================================= #
# ============================================================================================== #

# load and access the discord token, guild id and jikan url
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
jikanUrl = os.getenv("JIKAN_URL")
GUILD_RAW_ID = os.getenv("GUILD_ID")
if GUILD_RAW_ID:
  guildId = discord.Object(id=GUILD_RAW_ID)
else:
  guildId = None

# the main class that adds the bot's functionality
class Client(commands.Bot):

  async def on_ready(self):
    print(f'Logged on as {self.user}!')
    try:
      guild = discord.Object(id=1206133484423483453)
      synced = await self.tree.sync(guild=guild)
      print(f'Synced {len(synced)} commands to guild {guild.id}.')
    except Exception as e:
      print(f'Error syncing commands: {e}')

  async def on_message(self, message):
    if message.author == self.user:
      return
    if 'easter egg' in message.content.lower():
      await message.channel.send(f"You found the easter egg, {message.author}! 🐣")
      
  async def on_member_join(self, message, user):
    await message.channel.send(f"Hello there, {user}!")

  async def on_member_remove(self, message, user):
    await message.channel.send(f"Bye-bye, {user}!")

# allowing the bot to access the privilages set by the user
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

# ================================== LOAD AND SAVE JSON DATA =================================== #

DATA_FILE = "data.json"

def load_data(key, default_value=None):
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
      return json.load(f).get(key, default_value)
  return default_value

def save_data(key, value):
  data = {}
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
      data = json.load(f)
  data[key] = value
  with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

# ============================================================================================== #
# ======================================= SLASH COMMANDS ======================================= #
# ============================================================================================== #

# ======================================= COINFLIP ======================================= #

@client.tree.command(name="coinflip", description="Flips a coin.", guild=guildId)
async def rollDice(interaction: discord.Integration):
  roll = random.randint(1, 2)
  
  match roll:
    case 1:
      await interaction.response.send_message(f'🪙 The coin landed on: **Heads**!')
    case 2:
      await interaction.response.send_message(f'🪙 The coin landed on: **Tails**!')

# ======================================= DICE ROLL ======================================= #

@client.tree.command(name="roll-dice", description="Rolls a dice with however many sides you want.", guild=guildId)
async def rollDice(interaction: discord.Integration, sides: int):
  roll = random.randint(1, sides)

  await interaction.response.send_message(f'🎲 You rolled a **{roll}**!')

# =================================== MULTIPLE DICE ROLLS ==================================== #

@client.tree.command(name="roll-multiple-dice", description="Rolls any number of dice with however many sides you want.", guild=guildId)
async def rollManyDice(interaction: discord.Integration, dice: int, sides: int):
  countOfDice = 0

  totalRolls = []

  totalValue = 0

  for countOfDice in range(dice):
    roll = random.randint(1, sides)
    totalRolls.append(roll)
    countOfDice += 1

  for value in totalRolls:
    totalValue += value

  await interaction.response.send_message(f'🎲 You rolled: **{totalRolls}**!\n\n📊 Your total is: **{totalValue}**!')

# =================================== GET A RANDOM QUOTE ==================================== #

@client.tree.command(name="random-quote", description="Gives a random motivational quote.", guild=guildId)
async def randomQuoteGen(interaction: discord.Integration):
  quote = pyquotegen.get_quote()

  await interaction.response.send_message(f'{quote}')

# =================================== GET A USER'S AVATAR ==================================== #

@client.tree.command(name="user-avatar", description="Gets a user's avatar.", guild=guildId)
async def getUserAvatar(interaction: discord.Integration, user: discord.User):
  avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

  await interaction.response.send_message(avatar_url)

# =================================== GET A USER'S BANNER ==================================== #

@client.tree.command(name="user-banner", description="Gets a user's banner.", guild=guildId)
async def getUserBanner(interaction: discord.Integration, user: discord.User):
  user = await client.fetch_user(user.id)

  if user.banner:
    banner_url = user.banner.url  # Get the banner URL
    await interaction.response.send_message(banner_url)
  else:
    await interaction.response.send_message(f"{user.display_name} does not have a banner set.")

# ====================================== ASK THE 8BALL ====================================== #

@client.tree.command(name="8ball", description="Ask the 8ball a question and it will answer...", guild=guildId)
async def askEightBall(interaction: discord.Integration, question: str):
  
  responses = ["Yes", "No", "Maybe", "I think so.", "I don't think so.", "You're lying to yourself.", "My sources say no.", "I need a pay raise..."]

  randomNum = random.randint(0, len(responses))

  finalResponse = responses[randomNum]

  embed = discord.Embed(type='rich')
  embed.set_image(url="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDJxcjMzODFrOTZtZTh6eG96b29yNmNxaXJtdWwxZ3pmNm5xN2NldSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fkeLNBr7pdr0c/giphy.gif")
  embed.add_field(name="🎱 Your question", value=question, inline=False)
  embed.add_field(name="🎱 Your answer", value=finalResponse, inline=False)
  embed.color = discord.Color.random()

  await interaction.response.send_message(embed=embed)

# ====================================== GET A RANDOM ANIME ====================================== #

def get_random_anime():
  anime_id = random.randint(1, 20000)

  response = requests.get(f"{jikanUrl}/anime/{anime_id}")

  if response.status_code == 200:
    data = response.json()
    title = data["data"]["title"]
    url = data["data"]["url"] 
    return (f"Random Anime: {title}\nMore info: {url}")
  else:
    return (f"Failed to fetch anime with ID {anime_id}. Try again.")

@client.tree.command(name="random-anime", description="Get a random anime recommendation.", guild=guildId)
async def randomAnime(interaction: discord.Integration):
  await interaction.response.send_message(get_random_anime())

# ====================================== GET A RANDOM MANGA ====================================== #

def get_random_manga():
  manga_id = random.randint(1, 20000)

  response = requests.get(f"{jikanUrl}/manga/{manga_id}")

  if response.status_code == 200:
    data = response.json()
    title = data["data"]["title"]
    url = data["data"]["url"] 
    return (f"Random Manga: {title}\nMore info: {url}")
  else:
    return (f"Failed to fetch anime with ID {manga_id}. Try again.")
 
@client.tree.command(name="random-manga", description="Get a random manga recommendation.", guild=guildId)
async def randomManga(interaction: discord.Integration):
  await interaction.response.send_message(get_random_manga())

# ================================ GET A RANDOM ANIME CHARACTER ====================================== #

def get_random_anime_character():
  character_id = random.randint(1, 20000)

  response = requests.get(f"{jikanUrl}/characters/{character_id}")

  max_retries = 10
  retries = 0

  compatibility = random.randint(1, 100)
  compatibilityMessage = ''

  while retries < max_retries:
    if response.status_code == 200:
      data = response.json()
      name = data["data"]["name"]
      about = data["data"]["about"]
      url = data["data"]["url"]
      images = data["data"]["images"]["jpg"]["image_url"]

      if len(about) >= 1024:
        about = "The about section is too large, click the link below to learn more about the character!"

      if compatibility <= 25:
        compatibilityMessage = f"💔 You are {compatibility}% compatible... Just give up... 😭"
      elif 25 < compatibility <= 50:
        compatibilityMessage = f"💓 You are {compatibility}% compatible.. Maybe start looksmaxxing? 🤕"
      elif 50 < compatibility <= 75:
        compatibilityMessage = f"💖 You are {compatibility}% compatible. You might have a chance! 🙏"
      elif 75 < compatibility <= 90:
        compatibilityMessage = f"💞 You are {compatibility}% compatible! You're irresistible! 🥵"
      elif 90 < compatibility <= 100:
        compatibilityMessage = f"💘 You are {compatibility}% compatible!!! I present to you your future waifu/husbando. 🫡 "
      
      embed = discord.Embed(type='rich')
      embed.title = f"🥰 Your random waifu/husbando is... {name}"
      embed.add_field(name="About", value=about, inline=False)
      embed.add_field(name="Compatability %", value=compatibilityMessage, inline=False)
      embed.add_field(name="More Info", value=url, inline=False)
      embed.set_image(url=images)
      embed.color = discord.Color.random()

      return embed
    
    retries += 1
    
  embed = discord.Embed(
    title="Failed to fetch character 😢",
    description=f"Tried {max_retries} times but couldn't find a valid character. Try again.",
    color=discord.Color.red()
  )
  return embed

@client.tree.command(name="find-your-waifu", description="Find your perfect waifu/husbando!", guild=guildId)
async def randomCharacter(interaction: discord.Integration):
  embed = get_random_anime_character()
  await interaction.response.send_message(embed=embed)

# ====================================== CUSTOM EMBED ====================================== #

@client.tree.command(name="custom-embed", description="Make your own custom embed!", guild=guildId)
async def customEmbed(interaction: discord.Integration, 
  title: str = None,
  title_url: str = None,
  description: str = None,
  hex_color: str = None,
  thumbnail_url: str = None,
  big_image_url: str = None,
  field1_title: str = '',
  field1_value: str = '',
  field2_title: str = '',
  field2_value: str = '',
  field3_title: str = '',
  field3_value: str = '',
):
  if not (title or description or thumbnail_url):
    await interaction.response.send_message("You didn't provide any inputs!", ephemeral=True)
    return
  
  embed = discord.Embed(type='rich')
  embed.title = title
  embed.url = title_url
  embed.description = description
  embed.color = discord.Color.from_str(hex_color) if hex_color else discord.Color.random()
  embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
  embed.set_thumbnail(url=thumbnail_url)
  embed.add_field(name=field1_title, value=field1_value, inline=False)
  embed.add_field(name=field2_title, value=field2_value, inline=False)
  embed.add_field(name=field3_title, value=field3_value, inline=False)
  embed.set_image(url=big_image_url)

  await interaction.response.send_message(embed=embed)

# ================================== SIMPLE SLOT MACHINE ===================================== #

@client.tree.command(name="slot-machine", description="I'm a slot machine.", guild=guildId)
async def simpleSlotMachine(interaction: discord.Integration, bet: int):
  rows = 3
  cols = 3
  emojis = ['❌', '✅']
  matrix = [[random.choice(emojis) for _ in range(cols)] for _ in range(rows)]
  row_strings = []
  row_win = False
  col_win = False
  diagonal_win = False

  for row in matrix:
    row_string = ' '.join(row)  # Convert row to a string
    row_strings.append(row_string)  # Store the string
    if all(cell == '✅' for cell in row):
      row_win = True

  for col_idx in range(cols):
    if all(matrix[row_idx][col_idx] == '✅' for row_idx in range(rows)):
      col_win = True

  if all(matrix[i][i] == '✅' for i in range(rows)):  # Top-left to bottom-right diagonal
    diagonal_win = True
  if all(matrix[i][cols - i - 1] == '✅' for i in range(rows)):  # Top-right to bottom-left diagonal
    diagonal_win = True

  full_display = '\n'.join(row_strings)

  if row_win or col_win or diagonal_win:
    await interaction.response.send_message(f'{full_display}\n\nYou won ${bet}!')
  elif row_win and col_win or row_win and diagonal_win or col_win and diagonal_win:
    bet *= 2
    await interaction.response.send_message(f'{full_display}\n\nYou won ${bet}!')
  else:
    await interaction.response.send_message(f'{full_display}\n\nYou won nothing...')

# ======================================= TOTAL CLICKS ======================================= #

counter = load_data("counter", 0)
@client.tree.command(name="click", description="Increment a counter by 1, which is saved for all users.", guild=guildId)
async def incrementCounter(interaction: discord.Integration):
  global counter
  counter += 1
  save_data("counter", counter)
  await interaction.response.send_message(f"The counter is now: {counter}!")

# ============================================================================================== #
# ======================================== TEST COMMANDS ======================================= #
# ============================================================================================== #

# buttons
@client.tree.command(name="feet-pics", description="Free fit pics!", guild=guildId)
async def freeFeetPics(interaction: discord.Integration):
  view = discord.ui.View()
  button = discord.ui.Button(label = "👣 Free Fit Pics!", url="https://i.pinimg.com/236x/24/97/c2/2497c290c31e86f3adc15c670480b6c4.jpg")
  view.add_item(button)

  await interaction.response.send_message(view=view)






# ============================================================================================== #
# ========================================= RUN THE BOT ======================================== #
# ============================================================================================== #

# running the bot by passing in the functions and intents(permissions)
client.run(token)


