import requests
from exceptions import battlenet

class OverwatchService:
  def __sanitize_battletag(self, battletag: str):
    """Replace the default battletag format with the used by the API
    """
    return battletag.replace('#', '-')

  def get_profile(self, platform: str, battletag: str):
    sanitized_battletag = self.__sanitize_battletag(battletag)
    response = requests.get(f'https://ow-api.com/v1/stats/{platform}/us/{sanitized_battletag}/profile')

    data = response.json()

    if response.status_code == 404:
      raise battlenet.ProfileNotFound()

    if data['private']:
      raise battlenet.ProfilePrivate()

    return data
