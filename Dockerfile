FROM python:3.10.12

WORKDIR /home/python

COPY . .

RUN pip install -r requirements.txt

RUN prisma generate --schema=./schema/schema.prisma
