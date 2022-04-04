from django.conf import settings
from django.core.management import BaseCommand
from telegram.ext import Updater
from decouple import config
from sticker_maker.views import handler_objects


class Command(BaseCommand):
    help = 'Run the telegram bot'

    def handle(self, *args, **options):
        updater = Updater(token=config('BOT_TOKEN'))

        for handler in handler_objects:
            updater.dispatcher.add_handler(handler)

        updater.dispatcher.add_error_handler(lambda update, context: print(context.error))

        updater.start_polling()
        print(self.style.SUCCESS('[Bot started]'))
        updater.idle()
        print(self.style.NOTICE('[Bot stopped]'))
