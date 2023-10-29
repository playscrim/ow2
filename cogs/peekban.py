import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

from constants import MAP_POOL

class View(nextcord.ui.View):
  def __init__(self, view_cls, *args):
    super().__init__()
    self.add_item(view_cls(*args))

class MapSelect(nextcord.ui.Select):
  def __init__(self, map_pool):
    self.__map_pool = map_pool

    options = []

    for option in self.__map_pool:
      options.append(
        nextcord.SelectOption(label=option['name'], value=option['screenshot'])
      )

    super().__init__(
      placeholder='Pick a map to ban',
      max_values=1,
      min_values=1,
      options=options
    )

  async def callback(self, interaction: Interaction):
    def cb_filter(x):
      return x['screenshot'] != self.values[0]
    
    map_pool = list(filter(cb_filter, self.__map_pool))

    await interaction.response.send_message(
      f'You banned {self.values[0]}', 
      view=View(MapSelect, map_pool)
    )

class Peekban(commands.Cog):
  def __init__(self, client):
    self.client = client

  @nextcord.slash_command(
    name="peekban", 
    description="Map peek ban option"
  )
  async def peekban(
    self, 
    interaction: Interaction,
  ):
    await interaction.response.send_message(content='Hello', view=View(MapSelect, MAP_POOL['control']))

def setup(client):
  """Setup function to add cog to client
  """
  client.add_cog(Peekban(client))
