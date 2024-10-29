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
2. Run `make init` (or if you don't have make, run each line in Makefile on init section line-by-line).
3. Fill in the `.env` file with your own values.
4. View database revision history with `python -m alembic -n <service> history`.
5. Run `python -m alembic -n <service> upgrade <revision>` with the revision you need (set revision to head if using the latest version).

### Docker Installation

6. Run `make up-all` to start all services.

### Manual Installation

6. Add the following to `.env`:
```sh
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=faz
MYSQL_PASSWORD=password
MYSQL_FAZCORD_DATABASE=faz-cord
MYSQL_FAZDB_DATABASE=faz-db
```
7. Export the environment variables: `export $(grep -v '^#' .env | xargs)`
8. Run `mysql/init/0_init_users.sql` using your SQL client.
9. Run the service: `python -m <module-path>`

> [!NOTE]
> - Make sure you have MariaDB/MySQL and atleast Python 3.12 installed.
> - You have to do step 3 and 7 every time you open a new terminal.
> - Argument for step 8 is the path to the __main__.py file of the service you want to run. e.g., `fazbeat.api_collect`.
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
