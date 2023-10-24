from prisma.models import User

class UserService:
  def create_user(self, user_dto):
    return User.prisma().create(user_dto)
