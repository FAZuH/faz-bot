# faz-docker

Wynncraft utility and statistics discord bot. Inspired by motoki317's [moto-bot](https://github.com/motoki317/moto-bot/blob/master/README.md).

> [!WARNING]
> 
> This repository is currently in development phase, and may undergo many unstable and/or breaking changes.

## Development

Some useful shortcuts for development are written in `Makefile`.

- `make build` to (re-)build the image and launch the bot.
- `make up` to launch the bot (does not rebuild the image).
- `make down` to stop the bot and DB.

For debugging:

- `make bot-up` to launch only the faz-bot container.
- `make bot-down` to stop only the faz-bot container.
- `make bot-bash` to open bash shell on faz-bot container.
- `make bot` to attach to faz-bot container standard output.

- `make db-up` to launch only the faz-db container.
- `make db-down` to stop only the faz-db container.
- `make db-bash` to open bash shell on faz-db container.
- `make db` to attach to faz-db container standard output.

- `make sql-up` to launch only the DB container.
- `make sql-down` to stop only the DB container.
- `make sql-bash` to open bash shell on DB container.
- `make sql` to connect to DB (password: `password`).

Access your SQL database remotely through SSH by forwarding the remote port to a local port on your machine:

```sh
# Accessing database using phpMyAdmin on localhost:8080
ssh -L 8080:localhost:8080 user@remote-ip

# Accessing database using mariadb/mysql client on localhost:3306
ssh -L 3306:localhost:3306 user@remote-ip
```

## Production

You can either manually build and install the bot, or pull image from the release.
Using docker might be easier but overheads could be a problem in small servers.

### Docker Installation

1. Clone this repository.

```sh
git clone https://github.com/FAZuH/faz-docker.git

cd faz-docker
```

2. Create a file named `.env` and set environment variables (see `.env-example`).
3. Execute `docker-compose up -d`.
