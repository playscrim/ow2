import nextcord

from datetime import datetime
from ..services.overwatch import OverwatchService

from nextcord.ext import commands
from nextcord import Interaction, SlashOption

class Tracker(commands.Cog):
  """Tracker related commands
  """
  def __init__(self, client, overwatch: OverwatchService) -> None:
    self.client = client
    self.__overwatch = overwatch

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
    """Get player stats
    """
    status_code, data = self.__overwatch.get_profile(platform, battletag)

    author = interaction.user.mention

    if status_code == 404:
      return await interaction.response.send_message(f'{author}\nUser {battletag} not found, please try again!')
  
    competitive_stats = data['competitiveStats']
    matchs = competitive_stats['games']

    played = matchs['played']
    won = matchs['won']
    lost = played - won

    ratings = data['ratings']
    thumbnail = data['icon']

    description = []

    for rating in ratings:
      rank = rating['group']
      role = rating['role']
      tier = rating['tier']

      message = f'{role}: {rank} {tier}'
      description.append(message)

    d_message = '\n'.join(description)

    embed = nextcord.Embed(
      title=battletag,
      description=d_message,
      timestamp=datetime.utcnow(),
      color=nextcord.Colour.blurple()
    )

    embed.add_field(
      name='Matchs:',
      value=f'Played: {played}\nWon: {won}\nLost: {lost}'
    )

    embed.set_footer(text='https://playscrim.com')
    embed.set_thumbnail(url=thumbnail)

    await interaction.response.send_message(embeds=[embed])

def setup(client):
  """Setup function to add cog to client
  """
  overwatch = OverwatchService()
  client.add_cog(Tracker(client, overwatch))
