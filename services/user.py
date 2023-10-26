from prisma.models import User

class UserService:
  def __init__(self) -> None:
    self.__prisma = User.prisma()

  def create_user(self, user_dto):
    return self.__prisma.create(user_dto)

  def find_one(self, user_id):
    return self.__prisma.find_first(where={
      'user_id': user_id,
    })
