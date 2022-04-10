# warframe-telegram-bot

Available on [*Telegram*](https://t.me/warframe_void_fissures_bot).

Born to help:

- **Warframers:** allowing them to easily know about some missions.

<hr />
<br />

## Commands and Actions

| Command        | Description                             |
| -------------- | --------------------------------------- |
| `/help`        | List of commands.                       |
| `/language`    | Set a bot language.                     |
| `/info`        | Bot info / description.                 |
| `/time`        | Current world time in each earth.       |
| `/search`      | Search for a void fissure mission type. |
| `/sortie`      | Daily sortie.                           |
| `/trader`      | Void Trader time left.                  |
| `/arbitration` | Current arbitration mission.            |
| `/nightwave`   | Weekly nightwave missions.              |
| `/events`      | Warframe events.                        |


## Enviroment

| Field              | Description                                                        |
| ------------------ | ------------------------------------------------------------------ |
| `TOKEN`            | Telegram bot token given from [BotFather](https://t.me/botfather). |

<hr />
<br />

## Installing requirements

* Installation from source (requires git):

```
$ git clone https://github.com/Pandabug/warframe-telegram-bot.git
$ cd warframe-telegram-bot
```

* Installation of Libraries:

```bash
pip install -r requirements.txt
```

* Past API Token in `Constants.py` file and save it with name `TOKEN = ''`.

### Run
```
$ python main.py
```

To stop use `CTRL+C`


## Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/apps)


## License

Released under the [MIT](https://opensource.org/licenses/MIT) license.

This bot is built on top of [telebot](https://python-telegram-bot.readthedocs.io/en/stable/), distributed under MIT License.  