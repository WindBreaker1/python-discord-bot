

# ========================================= RPG GAME ======================================== #
class Creature:
  def __init__(self, name, description, image):
    self.name = name
    self.description = description
    self.image = image

dragon = Creature("Dragon", "Mystical lizard that breathes fire.", "https://i.pinimg.com/736x/3b/98/1d/3b981d0d8f5b7d92cdee2e668319a1c3.jpg")

rat = Creature("Rat", "A fucking rat", "https://i.pinimg.com/736x/dd/85/3b/dd853b5c3a874aed38b9a04c712809d1.jpg")

horror = Creature("Two-Legged Horror", "Unkown creature residing in the void. Will stop at nothing to consume you.", "https://i.pinimg.com/236x/ed/e2/79/ede279c0ce89f1bee52aafcaac28de83.jpg")

creatures = [dragon, rat, horror]

# @client.tree.command(name="codex_creature", description="Search the creature codex.", guild=guildId)
# async def codexCreatures(interaction: discord.Integration, query: str):
#   matching_creature = next((creature for creature in creatures if creature.name.lower() == query.lower()), None)
#   if matching_creature:
#     embed = discord.Embed(
#       title = matching_creature.name,
#       description = matching_creature.description,
#       color=discord.Color.green()
#     )
#     embed.set_image(url = matching_creature.image)
#     await interaction.response.send_message(embed=embed)
#   else:
#     await interaction.response.send_message(f'Search something else...')
