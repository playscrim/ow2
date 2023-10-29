import nextcord

from datetime import datetime

from helpers import messages
from services.overwatch import OverwatchService

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
    try:
      data = self.__overwatch.get_profile(platform, battletag)

      competitive_stats = data['competitiveStats']
      matchs = competitive_stats['games']

      played = matchs['played']
      won = matchs['won']
      lost = played - won

      ratings = data['ratings']
      thumbnail = data['icon']

      description = '\n'.join([f'{x["role"]}: {x["group"]} {x["tier"]}' for x in ratings])

      profile_embed = nextcord.Embed(
        title=battletag,
        description=description,
        color=nextcord.Colour.blurple(),
        timestamp=datetime.utcnow()
      )

      profile_embed.add_field(
        name='Matchs:',
        value=f'Played: {played}\nWon: {won}\nLost: {lost}'
      )

      profile_embed.set_footer(text='https://playscrim.com')
      profile_embed.set_thumbnail(url=thumbnail)

      await interaction.response.send_message(embeds=[profile_embed])

    except Exception as error:
      message_author = interaction.user
      error_embed = messages.error_embeds[type(error)]

      await interaction.response.send_message(
        content=message_author.mention, 
        embeds=[error_embed]
      )

def setup(client):
  """Setup function to add cog to client
  """
  overwatch = OverwatchService()
  client.add_cog(Tracker(client, overwatch))
