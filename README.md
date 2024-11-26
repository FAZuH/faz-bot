# faz-bot-app-discord

faz-bot Discord bot application

## Table of Contents

- [Installation](#installation)
    - [Requirements](#requirements)
    - [Steps](#steps)
- [Usage](#usage)
- [Bug Reports and Feature Requests](#bug-reports-and-feature-requests)
- [License](#license)

## Installation

### Requirements

- git: [git-scm.com](https://git-scm.com/downloads)
- uv: [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
- Docker: [docker.com](https://www.docker.com/)

### Steps

1. Clone this repository

```sh
git clone https://github.com/FAZuH/faz-bot-app-discord
```

Change directory into the repository using `cd faz-bot-app-discord`.

2. Set environment variables

Copy using `cp .env-example .env`, and fill the placeholders in `.env`.

3. Install and start a MySQL database with Docker

```sh
docker run -d \
    --name mysql \
    --restart unless-stopped \
    -e MYSQL_ROOT_PASSWORD=password \
    -p 127.0.0.1:3306:3306 \
    -v mysql_data:/var/lib/mysql \
    mariadb:11.4.2
```

4. Initialize the database

Run `uv run faz-initdb` to initialize the database.

> [!NOTE]
> - Database server that is not installed with Docker is currently not supported.
> - Application logs are stored on `logs` directory, in the root of the repository.

## Usage

Run the app using `uv run faz-discord`.

## Bug Reports and Feature Requests

You can report bug or request for features on the [issue tracker](https://github.com/FAZuH/faz-bot-app-discord/issues).

## License

`faz-bot-app-discord` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
