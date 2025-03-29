# Music Explorer: Rediscover Your Music Collection

Slimmed down to bare essentials for progress

## Start guide

### Preconditions

* Docker and Docker Compose V2 installed

### How to start using this

#### Setting up the environment

* Clone this repository
* I assumed you have python and [pip](https://python.land/virtual-environments/installing-packages-with-pip) installed.
* Create Python venv
  * ```python -m venv .venv```
* Install requirements:
  * ```pip install -e .```
* I assumed you have docker and docker compose v2 installed
* Start a redis docker container
  * ```sudo docker compose up -d```

#### Running the project

Run the celery worker to be able to debug the project:
    * Start the celery worker, make sure you keep this command running in a terminal. This allows the script to fire op load jobs:
       * ```celery --app=app_explorer.celery_config worker --loglevel=info```
    * Start a debug session with the file ```src/app_explorer/app.py``` from your editor of choice.
