import requests

class OverwatchService:
  def __sanitize_battletag(battletag: str):
    return battletag.replace('#', '-')

  def get_profile(self, platform: str, battletag: str):
    sanitized_battletag = self.__sanitize_battletag(battletag)
    response = requests.get(f'https://ow-api.com/v1/stats/{platform}/us/{sanitized_battletag}/profile')

    return response.status_code, response.json()
