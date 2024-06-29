# faz-docker

Docker deployment repository for faz-bot and faz-db. Inspired by motoki317's [moto-bot](https://github.com/motoki317/moto-bot/blob/master/README.md).

## Table of Contents

- [Table of Contents](#table-of-contents)

## Development

Some useful shortcuts for development are written in `Makefile`.

- `make build` to (re-)build the image and launch the bot.
- `make up` to launch the bot (does not rebuild the image).
- `make down` to stop the bot and DB.

For debugging:

- `make bot-up` to launch only the faz-bot container.
- `make bot-down` to stop only the faz-bot container.
- `make db-up` to launch only the faz-db container.
- `make db-down` to stop only the faz-db container.
- `make sql-up` to launch only the DB container.
- `make sql-down` to stop only the DB container.
- `make sql` to connect to DB (password: `password`).

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
