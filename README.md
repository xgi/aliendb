![AlienDB Header](./res/aliendb_header.png)

[![Build Status](https://travis-ci.org/xgi/aliendb.svg?branch=master)](https://travis-ci.org/xgi/aliendb) [![codecov](https://codecov.io/gh/xgi/aliendb/branch/master/graph/badge.svg)](https://codecov.io/gh/xgi/aliendb)

# About

[https://aliendb.info](https://aliendb.info)

AlienDB is an analytics platform for trending Reddit threads. It stores historical data for the top threads on Reddit at any given time, including karma trends and comment stats. More information is available at [https://aliendb.info/about](https://aliendb.info/about).

# Project structure

AlienDB is structured as 4 Docker services. 3 of these, `PostgreSQL`, `Redis`, and `RabbitMQ`, use images from the public Docker repository. The final one, `web` is built manually. The project makes use of [docker-compose](https://docs.docker.com/compose/) to handle service definitions.

The web container is overseen by `supervisor`, which ensures that the following backend services are kept active:

* Gunicorn, the WSGI server for the Django application.
* Nginx, the public-facing web server.
* Celery, a task manager used to periodically scrape Reddit data.
* Flower, a small non-public web server for monitoring Celery tasks.

The web app itself uses Django as a backend, with the majority of the application code in the `analytics` app which is found in `web/aliendb/apps/analytics`.

# Configuration

It is recommended that you create copies of the config files for development and production environments. For example, for a development environment:

```bash
cp docker-compose.yml docker-compose-dev.yml
cp .env .env-dev
```

You will need to update any references from .env to .env-dev in the docker-compose-dev.yml file.

## Praw

Most settings given in the provided .env file are suitable for development use. However, you will need to configure the Praw settings in order for the app to retrieve data from Reddit.

1. [Register a Reddit application.](https://github.com/reddit/reddit/wiki/OAuth2#getting-started) You should use the "script" classification.
2. Identify the client_id and client_secret keys from the app's information panel.
3. Fill in the necessary information in your env file.

# Building

1. Install [Docker](https://docs.docker.com/) and [docker-compose](https://docs.docker.com/compose/).
2. Build the Docker services:

```bash
docker-compose -f docker-compose-dev.yml build --no-cache
```

3. Create and start the Docker containers:

```bash
docker-compose -f docker-compose-dev.yml up [-d]
```

4. Connect to the website at `http://localhost`
5. Make any necessary changes to the code.
6. Stop and remove the `web` container.

```bash
docker-compose -f docker-compose-dev.yml stop web
docker-compose -f docker-compose-dev.yml rm web
```

7. Build the new image and create+start a new container.

```bash
docker-compose -f docker-compose-dev.yml up [-d] --build
```

# Testing

This project generally uses the generic testing framework provided by Django, which is itself based on Python's built-in `unittest` module. For general information about writing tests, see [Django's documentation](https://docs.djangoproject.com/en/2.0/topics/testing/) on the subject.

1. Start the containers using the above [Building](#building) instructions.
2. Run the appropriate `manage.py test` command on the running `web` container:

```bash
docker-compose -f docker-compose-dev.yml run --rm web \
    python manage.py test aliendb.apps.analytics.tests
```

# License

[3-Clause BSD License](https://github.com/xgi/aliendb/blob/master/LICENSE)