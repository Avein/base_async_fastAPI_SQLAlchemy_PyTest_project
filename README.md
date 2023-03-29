# Base async project using FastAPI, SQLAlchemy and PyTest


## How to app:
- Create your own `.env` file based on `.env_example` file
- `docker-compose up --build`

## How to tests:
You can run tests from inside of docker container e.g.
- `docker exec -it {docker container id} pytest /app/api/artists/tests.py`
- `docker exec -it {docker container id} pytest /app/api/healthcheck/tests.py`