import nextcord
import requests
from datetime import datetime

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
    """ Creating user request for player stats
        Validation status code response from API
    """
    response = requests.get(f"https://ow-api.com/v1/stats/{platform}/us/{battletag.replace('#', '-')}/profile")
    data = response.json()

    author = interaction.user.mention
    if response.status_code == 404:
      await interaction.response.send_message(f"{author} - User {battletag} not found, please try again!")
      return
  
    competitive_stats = data["competitiveStats"]
    matchs = competitive_stats["games"]
    played = matchs["played"]
    won = matchs["won"]
    ratings = data["ratings"]
    thumbnail = data['icon']

    description = []
    for i in ratings:
      elo = i["group"]
      role = i["role"]
      tier = i["tier"]

      message = f"{role}: {elo} {tier}"
      description.append(message)
    d_message = '\n'.join(description)

    embed = nextcord.Embed(
      title=battletag,
      description=d_message,
      timestamp=datetime.utcnow()
    )

    embed.set_footer(
      text="https://playscrim.com"
    )

    embed.add_field(
      name="Matchs:",
      value=f"Played: {played}\nWon: {won}"
    )

    embed.set_thumbnail(
      url=thumbnail
    )
    await interaction.response.send_message(embeds=[embed])

def setup(client):
  """Setup function to add cog to client
  """
  client.add_cog(Tracker(client))
