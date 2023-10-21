import os
import nextcord
from nextcord.ext import commands

from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config["TOKEN"]

class Client(commands.Bot):
  """Discord client
  """
  def __init__(self):
    super().__init__(intents=nextcord.Intents.all())

def bootstrap():
  client = Client()

  for cog in os.listdir('./cogs'):
    if cog.endswith('.py'):
      client.load_extension(f'cogs.{cog[:-3]}')

  client.run(TOKEN)

if __name__ == "__main__":
  bootstrap()
