# Credit Card Sticker Bot

This telegram-bot create sticker set from your credit cards number.
It is accessible via [telegram bot](https://t.me/credit_card_sticker_bot).

## Getting Started

If you want to run this bot on your own server, you can clone the repository and follow the instructions below:

Clone repository

```bash
git clone https://github.com/sadjadeb/credit_card_telegram_sticker_maker.git
```

### Prerequisite

Create an environment to run the app

```bash
cd credit_card_telegram_sticker_maker/
sudo apt-get install virtualenv
virtualenv venv
source venv/bin/activate
```

Install required libraries

```bash
pip install -r requirements.txt
```

Create config file

```bash
nano .env
```
You must set the following variables:
BOT_TOKEN, CHANNEL_ID, AD_STICKER_FILE_ID, DEBUG

## Run

to run the telegram-bot, you can use django command:

```bash
python manage.py runbot
```

and to run the webserver, run the following command:

```bash
python manage.py runserver
```

Now you can access the admin panel at http://localhost:8000/admin

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Give a ⭐️ if you like this project!

## License

[MIT](https://github.com/sadjadeb/credit_card_telegram_sticker_maker/blob/master/LICENSE)