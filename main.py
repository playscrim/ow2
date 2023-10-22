import re
import nextcord
from nextcord.ext import commands

from glob import glob
from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config["TOKEN"]

class Client(commands.Bot):
  """Discord client
  """
  def __init__(self):
    activity = nextcord.Game(
      name='Overwatch 2', 
      type=nextcord.ActivityType.playing
    )

    super().__init__(
      intents=nextcord.Intents.all(), 
      activity=activity, 
      status=nextcord.Status.do_not_disturb
    )

  async def on_ready(self):
    print('Bot is running')

def bootstrap():
  client = Client()

  for cog in glob('cogs/**/*.py', recursive=True):
    cog_ext = re.sub(r'\\|\/', '.', cog)
    client.load_extension(cog_ext[:-3])

  client.run(TOKEN)

if __name__ == "__main__":
  bootstrap()
