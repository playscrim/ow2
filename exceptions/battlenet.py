class ProfilePrivate(Exception):
  """Profile is private
  """
  def __init__(self):
    super().__init__('Profile is private')

class ProfileNotFound(Exception):
  """User not found
  """
  def __init__(self):
    super().__init__('User not found')
