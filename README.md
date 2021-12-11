# Flask App
This is an web application based on python-flask. It's supposed to manage an etl and an NLP process.

## Requirements
- Python 3.8 or higher

## Setup (as standalone locally)
1. Install requirements `pip install -r ./app/requirements`
2. Create .env file `cp ./app/.env.example ./app/.env` and use valid values
3. Run application `python ./app/main.py`
4. Access endpoint: http://localhost:5000

## Setup by using Docker-Compose
1. Create .env file `cp ./app/.env.example ./app/.env` and use valid values
2. Start docker by using `docker-compose up`
3. Access endpoint: http://localhost:5000
