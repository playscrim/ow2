import asyncio
from prisma import Prisma

async def main() -> None:
    prisma = Prisma()

    await prisma.connect()
    user = await prisma.user.create(
        
      data={
          
        'battletag': 'ŦȂyŎ#1524',
        'userid': 432354788219420683

      }

    )

if __name__ == '__main__':
    asyncio.run(main())