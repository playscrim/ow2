import nextcord

from nextcord.ext import commands
from nextcord import Interaction, ChannelType, SlashOption

class Match(commands.Cog):
  def __init__(self, client) -> None:
    self.client = client

  @nextcord.slash_command(name="create_scrim", description="Create a scrim match")
  async def create_scrim(self, interaction: Interaction):
    embed = nextcord.Embed(title="Uma nova partida está prestes a começar")

def setup(client):
  """Setup function to add cog to client
  """
  client.add_cog(Match(client))
