import nextcord

from nextcord.ext import commands
from nextcord.abc import GuildChannel

from nextcord import Interaction, ChannelType, SlashOption

class JoinButton(nextcord.ui.View):
  """UI Buttons to setup the role
  """
  def __init__(self) -> None:
    super().__init__()

  @nextcord.ui.button(
    label='Join as Tank',
    emoji='<:tank_role:1165467905962545272>',
    style=nextcord.ButtonStyle.blurple
  )
  async def join_match_as_tank(
    self, 
    button: nextcord.ui.Button, 
    interaction: Interaction
  ):
    await interaction.response.edit_message(content=f'{interaction.user}')
    await interaction.response.send_message('Joined as Tank', ephemeral=True)

  @nextcord.ui.button(
    label='Join as DPS',
    emoji='<:dps_role:1165474096319053934>',
    style=nextcord.ButtonStyle.blurple,
  )
  async def join_match_as_dps(
    self, 
    button: nextcord.ui.Button, 
    interaction: Interaction
  ):
    await interaction.response.edit_message(content=f'{interaction.user}')
    await interaction.response.send_message('Joined as DPS', ephemeral=True)

  @nextcord.ui.button(
    label='Join as Sup',
    emoji='<:sup_role:1165468265510871110>',
    style=nextcord.ButtonStyle.blurple,
  )
  async def join_match_as_sup(
    self, 
    button: nextcord.ui.Button, 
    interaction: Interaction
  ):
    await interaction.response.edit_message(content=f'{interaction.user}')
    await interaction.response.send_message('Joined as sup', ephemeral=True)

  @nextcord.ui.button(
    label='Cancel Match', 
    style=nextcord.ButtonStyle.red,
  )
  async def cancel_match(
    self, 
    button: nextcord.ui.Button, 
    interaction: Interaction
  ):
    await interaction.message.delete()
    await interaction.response.send_message('Match canceled', ephemeral=True)

class CreateMatchModal(nextcord.ui.Modal):
  """UI Modal to setup our match
  """
  def __init__(self, client, channel_id: str) -> None:
    super().__init__(
      title="Setup Match"
    )

    self.client = client
    self.channel_id = channel_id

    self.name = nextcord.ui.TextInput(
      label="Your match name",
      min_length=4,
      max_length=16
    )

    self.add_item(self.name)

  async def callback(self, interaction: Interaction):
    embed = nextcord.Embed(
      description='<a:loading:1165474674222829648> Waiting for players',
      color=nextcord.Colour.blurple()
    )

    join_button = JoinButton()

    await interaction.response.send_message(
      'Match created successfully!',
      ephemeral=True
    )

    target_channel = self.client.get_channel(self.channel_id)

    await target_channel.send(
      embeds=[embed], 
      view=join_button
    )

class Match(commands.Cog):
  """Match related commands
  """
  def __init__(self, client) -> None:
    self.client = client

  @nextcord.slash_command(
    name="create_match", 
    description="Create a scrim match"
  )
  async def create_match(
    self, 
    interaction: Interaction,
    map_pool = SlashOption(
      name='map_pool',
      description='Toggle map pick and ban',
      choices=['Enabled', 'Disabled']
    )
  ):
    create_match_modal = CreateMatchModal(self.client, '1165476045424705666') # queue channel
    await interaction.response.send_modal(create_match_modal)

def setup(client):
  """Setup function to add cog to client
  """
  client.add_cog(Match(client))
