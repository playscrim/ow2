import nextcord
import requests

from nextcord.ext import commands
from nextcord import Interaction, SlashOption

class Tracker(commands.Cog):
  """Tracker related commands
  """
  def __init__(self, client) -> None:
    self.client = client

  @nextcord.slash_command(
    name="tracker", 
    description="Get user stats"
  )
  async def tracker(
    self, 
    interaction: Interaction,
    platform = SlashOption(
      name='platform',
      description='Enter user platform to get user stats',
      choices=['pc', 'xbl', 'psn']
    ),
    battletag = SlashOption(
      name='battletag',
      description='Enter user battletag to get user stats'
    )
  ):
    request = request.get(f"https://ow-api.com/v1/stats/{platform}/us/{battletag}/profile") 

    # GET https://ow-api.com/v1/stats/:platform/:region/:battletag/profile
    await interaction.response.send_message('')

def setup(client):
  """Setup function to add cog to client
  """
  client.add_cog(Tracker(client))
