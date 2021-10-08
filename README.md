# Simple Open Dollar Cost Averaging (DCA) Bot

SimpleDCABot is a simple bot that buys crypto on a selected exchange at regular intervals for a prescribed amount in a defined period.  SimpleDCABot can run entirely independently or announce each purchase via chat on Telegram. 

Functionality is intentionally limited to the minimum necessary. This should make it easier to understand and verify the behavior of SimpleDCABot. 


Usage
```
usage: bot_main.py [-h] [--json JSON] [--test]

arguments:
  -h, --help   show this help message and exit
  --json JSON  Json bot configuration.
  --test       Bot test mode. Bot will comunicate, but it will never byu anything.

```

## Install
Please install the necessary packages before running bot. 
```
pip install -r requirements.txt
```
## JSON configuration

The JSON configuration contains all the necessary parameters. 

### Example

```
{
    "exchange": "coinbase",
    "crypto": "BTC",
    "fiat": "EUR",
    "amount": 10.0,
    "interval": 86400,
    "start": 10,
    "logfile": "./log.txt",
    "exchange_api": {
        "SECRET_KEY": "SOME_SECRET_KEY_DFDFDFASDFSDFSDFSDFSDF",
        "API_KEY": "API_KEY_VFVDFGEDFGDFGDFG",
        "PASSPHRASE": "PASSPHRASE_GRTEGEGRE"
    },
    "telegram_api": {
        "chat_id": "CHAT_ID_516+1464",
        "TOKEN": "TOKEN_5sdf61sd6f51"
    }
}
```
### The meaning of variables 

```
"exchange": Selected exchange platform. So far, only Coinbase Pro is supported. 
"crypto": Cryptocurrency to buy. 
"fiat": Selected fiat currency to spend.
"amount": How much will be spent on every purchase.
"interval": Waiting time for the next purchase in seconds.
"start": Waiting time for the first purchase in seconds.
"logfile": Path to log file.
"exchange_api": Coinbase Pro keys an passphrase for you api.
"telegram_api": Telegram token and chat id for Telegram bot. If the Telegram API is missing, it will not be used, and the bot will only log to the selected file and the terminal. 
```

## API requirements (Coinbase Pro)
 - View
 - Trade

## Telegram bot
Instructions on how to create your own Telegram bot and get its token can be found here: 
https://core.telegram.org/bots#botfather


## Plans and progress
### To Do
- [ ] Kraken support
- [ ] Binance support
- [ ] Functionality for dollar cost averaging sell
- [ ] Email comunication
- [ ] AdvancedDCABot - An advanced variant of the robot enables more advanced trading strategies, such as buying a dip.

### Done
- [X] Telegram message when order created 
- [X] Bot will validate chat_id
- [X] Bot will check balance of fiat
- [X] Test mode 


## Warning
Please check the functionality of this robot. 
Even if the robot is under your control, never give it an API with the ability to move your fund. 
Check regularly that it works as you expect. 
I make no guarantees that the robot is error-free and will work as you expect.
