import nextcord

from datetime import datetime
from exceptions import battlenet

error_embeds = {
  battlenet.ProfilePrivate: nextcord.Embed(
    color=nextcord.Color.from_rgb(255, 195, 0),
    description='This account is Private. If you\'re the account owner please consider making your profile public. You can change your profile visibility with the following steps: Options > Social > Career Profile Visibility click the arrows to select the public view. :unlock:',
    timestamp=datetime.utcnow()
  ),
  battlenet.ProfileNotFound: nextcord.Embed(
    color=nextcord.Color.red(),
    description=':x: User not found, please try again!'
  )
}

