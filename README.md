# warframe-telegram-bot

Available on [*Telegram*](https://t.me/warframe_void_fissures_bot).

Born to help:

- **Warframers:** allowing them to easily know about some missions.

<hr />
<br />

## Commands and Actions

| Command        | Description                                |
| -------------- | ------------------------------------------ |
| `/help`        | Show list of commands.                     |
| `/language`    | Set favorite language.                     |
| `/info`        | Show list of commands / description.       |
| `/time`        | Get the current time on planets.           |
| `/search`      | Search for void fissure missions.          |
| `/sortie`      | Get the details on the current Sortie.     |
| `/trader`      | Shows the Void Trader time and location.   |
| `/arbitration` | Get current arbitration mission.           |
| `/nightwave`   | Shows the daily and weekly nightwave acts. |
| `/events`      | Show warframe events.                      |
| `/tenshin`     | Show weekly tenshin reward.                |
| `/news`        | The latest news from warframe.             |


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

* Create file `Constants.py`

Constants.py
```
TOKEN = 'TOKEN'
MONGODB_URL = 'MONGODB_URL'
```
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