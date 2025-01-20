# the codex
class Creature:
  def __init__(self, name, description, image):
    self.name = name
    self.description = description
    self.image = image

dragon = Creature("Dragon", "Mystical lizard that breathes fire.", "https://i.pinimg.com/736x/3b/98/1d/3b981d0d8f5b7d92cdee2e668319a1c3.jpg")

rat = Creature("Rat", "A fucking rat", "https://i.pinimg.com/736x/dd/85/3b/dd853b5c3a874aed38b9a04c712809d1.jpg")

horror = Creature("Two-Legged Horror", "Unkown creature residing in the void. Will stop at nothing to consume you.", "https://i.pinimg.com/236x/ed/e2/79/ede279c0ce89f1bee52aafcaac28de83.jpg")

creatures = [dragon, rat, horror]