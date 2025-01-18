# to install discord library: <python3 -m pip install -U discord.py>
import discord
from discord.ext import commands
from discord import app_commands
# to install dotenv library: <pip install python-dotenv>
from dotenv import load_dotenv
import os
import random
import pyquotegen

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


# slash commands

@client.tree.command(name="drunk", description="I will print drunk text.", guild=guildId)
async def drunkPrinter(interaction: discord.Integration, query: str):
  await interaction.response.send_message(f'*hic* {query} *hic*')

@client.tree.command(name="d6", description="Rolls a d6.", guild=guildId)
async def rollDice(interaction: discord.Integration):
  roll = random.randint(1,6)
  await interaction.response.send_message(f'You rolled a 🎲{roll}!')

@client.tree.command(name="random_quote", description="Gives a random motivational quote.", guild=guildId)
async def randomQuoteGen(interaction: discord.Integration):
  quote = pyquotegen.get_quote()
  await interaction.response.send_message(f'{quote}')

# embeds

@client.tree.command(name="embed", description="Embed Demo", guild=guildId)
async def embedDemo(interaction: discord.Integration):
  embed = discord.Embed(
    title="Do not Click!",
    url="https://rule34.xxx/", 
    description="❌❌❌", 
    color=discord.Color.green()
    )
  embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
  embed.set_thumbnail(url='https://i.pinimg.com/236x/81/a4/5b/81a45bcf125c0ffb107c617cbd219fab.jpg')
  embed.add_field(name="The horrors...", value="...of the internet.", inline=False)
  embed.set_image(url='https://i.pinimg.com/236x/58/fe/99/58fe99f7127036ebeb30055bcb87dc59.jpg')
  await interaction.response.send_message(embed=embed)



# running the bot by passing in the functions and intents(permissions)
client.run(token)


