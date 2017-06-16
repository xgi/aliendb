# AlienDB

## Overview

AlienDB is an analytics platform for trending Reddit threads. It stores historical data for the top threads on Reddit at any given time, including karma trends and comment stats. More information is available at https://aliendb.info/about.

## Project structure
AlienDB is structured as 4 Docker services. 3 of these, `PostgreSQL`, `Redis`, and `RabbitMQ`, use images from the public Docker repository. The final one, `web` needs to be built manually. The project makes use of [docker-compose](https://docs.docker.com/compose/) to handle service definitions.

The web app itself uses Django as a backend. The main code is put in the app called 'analytics' which is found in `web/aliendb/apps/analytics`. Celery is used to automate scheduled tasks, notably the `get_top_submissions` task, which retrieves the top 100 posts on /r/all to update their stats.

## Configuration
It is recommended that you create copies of the config files for development and production environments. For example, for a development environment:
```bash
cp docker-compose.yml docker-compose-dev.yml
cp .env .env-dev
```
You will need to update any references from .env to .env-dev in the docker-compose-dev.yml file.

### Environmental variables
Most settings given in the provided .env file are suitable for development use. However, you will need to configure the Praw settings in order for the app to retrieve data from Reddit.

#### Praw

1. [Register a Reddit application.](https://github.com/reddit/reddit/wiki/OAuth2#getting-started) You should use the "script" classification.
2. Identify the client_id and client_secret keys from the app's information panel.
3. Fill in the necessary information in your env file.


## Building
1. Install [Docker](https://docs.docker.com/) and [docker-compose](https://docs.docker.com/compose/).
3. Build the Docker services:
```bash
docker-compose -f docker-compose-dev.yml build --no-cache
```
4. Create and start the Docker containers:
```bash
docker-compose -f docker-compose-dev.yml up [-d]
```
5. Connect to the website at http://localhost
6. Make any necessary changes to the code.
7. Stop and remove the `web` container.
```bash
docker-compose -f docker-compose-dev.yml stop web
docker-compose -f docker-compose-dev.yml rm web
```
8. Build the new image and create+start a new container.
```bash
docker-compose -f docker-compose-dev.yml up [-d] --build
```
