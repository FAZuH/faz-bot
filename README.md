# faz-bot

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

- `make bot [build|up|down|bash]` Manage container related to fazbot service.
- `make db [build|up|down|bash]` Manage container related to fazdb service.
- `make sql [build|up|down|bash]` Manage container related to mysql service.

Actions:
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
Using docker might be easier but overheads could be a problem in small servers.

### Docker Installation

1. Clone this repository.

```sh
git clone https://github.com/FAZuH/faz-bot.git

cd faz-bot
```

2. Create a file named `.env` and set environment variables (see `.env-example`).
3. Execute `docker-compose up -d`.
