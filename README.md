# Nothub

To install and start this project, run the following commands:

```
git clone https://github.com/triskattie/nothub.git
cd nothub
cp .env.example .env
docker compose up -d
```
You may want to edit values in `.env`, depending on how you want your environment setup.

To update this project, run the following commands:
```
git pull
docker compose up -d
```
To use a specific release, set the `NOTHUB_VERSION` in `.env`


## Tech stack
Python with Fastapi
Docker compose
PostgreSQL with Alembic for migrations