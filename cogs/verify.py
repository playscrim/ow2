import nextcord

from nextcord.ext import commands
from nextcord import Interaction

class LoginButton(nextcord.ui.View):
  """Login button that uses the OAuth API
  """
  def __init__(self) -> None:
    super().__init__()

  @nextcord.ui.button(
    label='Login with Battle.net', 
    emoji='<:BattleNet:1165471078160793660>',
    style=nextcord.ButtonStyle.blurple
  )
  async def login_with_battlenet(
    self,
    button: nextcord.ui.Button, 
    interaction: Interaction
  ):
    await interaction.response.send_message('Button clicked')

class Verification(commands.Cog):
  """Verification command
  """
  def __init__(self, client) -> None:
    self.client = client

  @nextcord.slash_command(name='verify', description='Verify user')
  async def verify_user(self, interaction: Interaction):
    login_button = LoginButton()

    verify_embed = nextcord.Embed(
      description='We need to verify your battle.net account', 
      color=nextcord.Colour.blurple()
    )

    await interaction.response.send_message(
      embeds=[verify_embed],
      view=login_button
    )

def setup(client):
  """Setup function to add cog to client
  """
  client.add_cog(Verification(client))
