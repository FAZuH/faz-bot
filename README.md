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

- `make fazcord [pull|build|up|down|bash]` Manage container related to fazcord service.
- `make fazcollect [pull|build|up|down|bash]` Manage container related to fazcollect service.
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

## Installation

You can either manually build and install the bot, or pull image from the release.
Using docker might be easier but overheads could be a problem.

**Dependencies**:
- Bash terminal (see [Git Bash](https://git-scm.com/downloads) for windows)
- Atleast Python 3.12 (tested up to Python 3.13.0)
- MariaDB/MySQL
- GNU Make

1. Clone the repository:

```sh
git clone https://github.com/FAZuH/faz-bot.git

cd faz-bot
```
2. Run `make init`
3. Fill in the `.env` file with your own values.

> [!NOTE]
> You can override python executable by setting `PYTHON` when calling make commands. e.g., `make init PYTHON=python3.13`

### Docker Installation

4. Run `make sql act=up wait-for-mysql initdb up-all` to pull, initialize, and start the service in one go.

After installing, you can just do step 5 to start all services.

### Manual Installation

4. Export the environment variables: `source .env`
5. Run `make initdb` to initialize the database.
6. Run `source .venv/bin/activate` to activate the virtual environment.
7. Run the service: `python -m <module-path>`

After running all the above, you just need to do step 4, 6 and 7 to start the service.

> [!NOTE]
> - Argument for step 7 is the module path to the __main__.py file of the service you want to run. e.g., `fazbeat.fazcollect`
> - Currently database version checking is not supported on manual installation. You just have to read the error.

## Changing Database Versions

To upgrade or downgrade the database version, you can use `alembic` to manage the database migrations. Make sure you have it installed by running `pip install alembic`.

1. View revision GUIDs with `python -m alembic --name <db-name> history`
2. Select the revision you want to checkout into `python -m alembic --name <db-name> upgrade <revision>`

Alternatively, you can upgrade straight to the latest revision by running `python -m alembic --name <db-name> upgrade head`.

> [!WARNING]
> - It is recommended to backup your database before upgrading/downgrading.
> - Downgrading might result in data loss.

## Credits

- [Wynncraft](https://wynncraft.com/): API for Wynncraft data.
- [moto-bot](https://github.com/motoki317/moto-bot/blob/master/README.md): Code inspiration. Mostly on structure.
- afterfive: Algorithm for computing probabilities of crafted item rolls.
