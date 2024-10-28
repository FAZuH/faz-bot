# faz-bot

Wynncraft utility and statistics discord bot. Inspired by motoki317's .

> [!WARNING]
> This repository is currently in development phase, and may undergo many unstable and/or breaking changes.

## Development

Some useful shortcuts for development are written in `Makefile`.

- `make build-all` to (re-)build the image and all services.
- `make up-all` to launch all services (does not rebuild the image).
- `make down-all` to stop all services.

For debugging:

- `make bot [pull|build|up|down|bash]` Manage container related to fazcord service.
- `make api-collect [pull|build|up|down|bash]` Manage container related to api_collect service.
- `make sql [pull|build|up|down|bash]` Manage container related to mysql service.

Actions:

- `pull` pull the image of the service without starting the service.
- `build` to (re-build) the image and launch the service.
- `up` to launch to launch the service (does not rebuild the image).
- `down` to stop the service.
- `bash` to open bash shell on the container.
- Empty action to attach to the service's standard output.

Access your SQL database remotely through SSH by forwarding the remote port to a local port on your machine:

```sh
# Accessing database using phpMyAdmin on localhost:8080
ssh -L 8080:localhost:8080 user@remote-ip

# Accessing database using mariadb/mysql client on localhost:3306
ssh -L 3306:localhost:3306 user@remote-ip
```

## Production

You can either manually build and install the bot, or pull image from the release.
Using docker might be easier but overheads could be a problem.

1. Clone the repository:

```sh
git clone https://github.com/FAZuH/faz-bot.git

cd faz-bot
```

### Docker Installation

2. Create a file named `.env` and fill in the environment variables (see `.env-example`)
3. Execute `docker-compose up -d`

### Manual Installation

2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements-dev.txt`.
5. Create a file named `.env` and fill in the environment variables (see `.env-example`).
6. Export the environment variables: `export $(grep -v '^#' .env | xargs)`
7. Run the service: `python -m <path-to-services-mainpy>`

> [!NOTE]
> - You have to do step 3 and 6 every time you open a new terminal.
> - Argument for step 7 is the path to the __main__.py file of the service you want to run. e.g., `fazbeat.api_collect`.
> - Currently database version checking is not supported on manual installation.

## Changing Database Versions

To upgrade or downgrade the database version, you can use `alembic` to manage the database migrations. Make sure you have it installed by running `pip install alembic`.

1. Pull latest git commit: `git pull origin main`
2. View revision GUIDs with `python -m alembic --name <db-name> history`
3. Select the revision you want to checkout into `python -m alembic --name <db-name> upgrade <revision>`

Alternatively, you can upgrade to the latest revision by running `python -m alembic --name <db-name> upgrade head`.

> [!WARNING]
> - It is recommended to backup your database before upgrading/downgrading.
> - Downgrading could potentially result in data loss.

## Credits

- [Wynncraft](https://wynncraft.com/): API for Wynncraft data.
- [moto-bot](https://github.com/motoki317/moto-bot/blob/master/README.md): Code inspiration. Mostly on structure.
- afterfive: Algorithm for computing probabilities of crafted item rolls.
