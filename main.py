# to install discord library: <python3 -m pip install -U discord.py>
import discord
from discord.ext import commands
from discord import app_commands
# to install dotenv library: <pip install python-dotenv>
from dotenv import load_dotenv
import os
import random
import pyquotegen
import requests

# load and access the discord token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
guildId = discord.Object(id=os.getenv("GUILD_ID"))

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
    if message.content.startswith('hello'):
      await message.channel.send(f'Hi there {message.author}.')
    if 'bye' in message.content.lower():
      await message.channel.send(f"Bye, bye {message.author}! 🥹")
    if 'fuck' in message.content.lower():
      await message.channel.send(f"Fuck you, too, {message.author}! 🤬")
       

  async def on_reaction_add(self, reaction, user):
    await reaction.message.channel.send(f'You reacted with {reaction}!')



# allowing the bot to access the privilages set by the user
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


# ======================================= SLASH COMMANDS =================================== #

@client.tree.command(name="drunk", description="I will print drunk text.", guild=guildId)
async def drunkPrinter(interaction: discord.Integration, query: str):
  await interaction.response.send_message(f'*hic* {query} *hic*')

# dice commands

@client.tree.command(name="coinflip", description="Flips a coin.", guild=guildId)
async def rollDice(interaction: discord.Integration):
  roll = random.randint(1, 2)
  if roll == 1:
    await interaction.response.send_message(f'🪙 The coin lands on: Heads!')
  elif roll == 2:
    await interaction.response.send_message(f'🪙 The coin lands on: Tails!')

@client.tree.command(name="dice", description="Rolls a dice with however many sides you want.", guild=guildId)
async def rollDice(interaction: discord.Integration, sides: int):
  roll = random.randint(1, sides)
  await interaction.response.send_message(f'🎲 You rolled a {roll}!')

@client.tree.command(name="multiple-dice", description="Rolls a number of dice with however many sides you want.", guild=guildId)
async def rollDice(interaction: discord.Integration, dice: int, sides: int):
  countOfDice = 0
  totalRolls = []
  totalValue = 0
  for countOfDice in range(dice):
    roll = random.randint(1, sides)
    totalRolls.append(roll)
    countOfDice += 1
  for value in totalRolls:
    totalValue += value
  await interaction.response.send_message(f'🎲 You rolled: {totalRolls}! \n 🎰 Your total is: {totalValue}!')

# slot machine
@client.tree.command(name="slot-machine", description="I'm a slot machine.", guild=guildId)
async def drunkPrinter(interaction: discord.Integration, bet: int):
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

# get a user's avatar

@client.tree.command(name="user-avatar", description="Gets a user's avatar.", guild=guildId)
async def getUserAvatar(interaction: discord.Integration, user: discord.User):
  avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
  await interaction.response.send_message(f"{user.display_name}'s avatar: {avatar_url}")









# random quotes

@client.tree.command(name="random_quote", description="Gives a random motivational quote.", guild=guildId)
async def randomQuoteGen(interaction: discord.Integration):
  quote = pyquotegen.get_quote()
  await interaction.response.send_message(f'{quote}')

# embeds

@client.tree.command(name="embed", description="Embed Demo", guild=guildId)
async def embedDemo(interaction: discord.Integration, query: str):
  embed = discord.Embed(
    title="Do not Click!",
    url="https://rule34.xxx/",
    description="❌❌❌",
    color=discord.Color.green()
    )
  embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
  embed.set_thumbnail(url='https://i.pinimg.com/236x/81/a4/5b/81a45bcf125c0ffb107c617cbd219fab.jpg')
  embed.add_field(name="Title", value=query, inline=False)
  embed.set_image(url='https://i.pinimg.com/236x/58/fe/99/58fe99f7127036ebeb30055bcb87dc59.jpg')
  await interaction.response.send_message(embed=embed)

# anime info slash command
BASE_URL = "https://api.jikan.moe/v4"
def get_random_anime():
  anime_id = random.randint(1, 15000)
  try:
      # Fetch data about the random anime
      response = requests.get(f"{BASE_URL}/anime/{anime_id}")
      # Check if the request was successful
      if response.status_code == 200:
          data = response.json()  # Parse JSON response
          title = data["data"]["title"]  # Access the 'title' key
          url = data["data"]["url"]  # Get the MyAnimeList URL
          return f"Random Anime: {title}\nMore info: {url}"
      else:
          # Handle cases where the ID is invalid
          return f"Failed to fetch anime with ID {anime_id}. Trying again..."
  except Exception as e:
      return f"An error occurred: {e}"

@client.tree.command(name="random-anime", description="Get a random anime.", guild=guildId)
async def randomAnime(interaction: discord.Integration):
  await interaction.response.send_message(f'{get_random_anime()}')


# running the bot by passing in the functions and intents(permissions)
client.run(token)


