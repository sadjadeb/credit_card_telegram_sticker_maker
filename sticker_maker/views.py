from typing import Dict
from telegram import Update, error, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CommandHandler, ConversationHandler
from decouple import config
from sticker_maker.renderer import cc_renderer
import logging

logger = logging.getLogger(__name__)

updater = Updater(token=config('BOT_TOKEN'))

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['وارد کردن اسم', 'وارد کردن شماره کارت'],
    ['ساخت پک استیکر'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

__to_english_nums__ = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')


def start(update: Update, context: CallbackContext):
    Welcome_message = f"""سلام {update.message.chat.first_name}
خیلی خوش اومدی!
برای ساخت استیکر شماره کارتت دستور /create رو بزن😁
"""

    first_name = update.message.chat.first_name if update.message.chat.first_name is not None else ''
    last_name = update.message.chat.last_name if update.message.chat.last_name is not None else ''
    username = update.message.chat.username
    context.bot.send_message(chat_id=update.effective_chat.id, text=Welcome_message)

    # log starts in channel
    context.bot.send_message(chat_id=config('CHANNEL_ID'),
                             text=f'{first_name} {last_name} with username @{username} started bot.',
                             disable_notification=True)
    # log starts in logger
    logger.info(f'{first_name} {last_name} with username {username} started bot')


def prettify_data(user_data: Dict[str, str]) -> str:
    """
    Helper function for formatting the gathered user info.
    """
    if len(user_data['cards']) == 0:
        text = "شماره کارتی وارد نشده!"
    else:
        text = f"شماره کارت ها: {', '.join(user_data['cards'])}"

    if user_data['name'] is not None:
        text += f"\nنام: {user_data['name']}"
    else:
        text += "\nنام وارد نشده!"

    return text


def create(update: Update, context: CallbackContext) -> int:
    """
    Start the conversation and ask user for input.
    """
    update.message.reply_text(
        "برای ساخت پک استیکر شماره کارتت، اطلاعاتت رو وارد کن🤑",
        reply_markup=markup,
    )
    context.user_data['cards'] = []
    context.user_data['name'] = None

    sticker_set_unique_name = update.effective_user.id
    try:
        sticker_set = context.bot.getStickerSet(name=f'cc_{sticker_set_unique_name}_by_credit_card_sticker_bot')
        previous_sticker = sticker_set.stickers[0]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'قبلا تو این ربات استیکر ساختی. اگر میخوای دوباره بسازی ادامه بده وگرنه استیکرت رو میتونی ببینی😁')
        context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=previous_sticker)
    except error.TelegramError:
        pass
    except IndexError:
        logger.warning(f'user {update.effective_user.id} previous sticker had no stickers')

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    """
    Ask the user for info about the selected predefined choice.
    """
    text = update.message.text
    context.user_data['choice'] = text
    if text == 'وارد کردن اسم':
        update.message.reply_text("اسمت رو بنویس:")
    elif text == 'وارد کردن شماره کارت':
        update.message.reply_text(f'شماره کارتت رو وارد کن:')

    return TYPING_REPLY


def received_information(update: Update, context: CallbackContext) -> int:
    """
    Store info provided by user and ask for the next item.
    """
    command = context.user_data['choice']
    input_value = update.message.text

    if command == 'وارد کردن اسم':
        context.user_data['name'] = input_value
    elif command == 'وارد کردن شماره کارت':
        input_value = input_value.replace(' ', '').replace('-', '')
        input_value = input_value.translate(__to_english_nums__)

        if len(input_value) != 16:
            update.message.reply_text("شماره کارت باید 16 رقم باشه! دوباره شماره کارتت رو وارد کن:")
            return TYPING_REPLY
        context.user_data['cards'].append(input_value)

    del context.user_data['choice']

    update.message.reply_text(
        f"""تا الان این اطلاعات رو به من دادی:
{prettify_data(context.user_data)}
میتونی بازم شماره کارت وارد کنی یا روی ساخت پک استیکر بزنی تا برات استیکرت رو بسازم😎
""",
        reply_markup=markup,
    )

    return CHOOSING


def create_cc_sticker_set(update: Update, context: CallbackContext) -> int:
    """
    Create sticker set from gathered data.
    """
    if 'choice' in context.user_data:
        del context.user_data['choice']

    name = context.user_data['name']
    cards = context.user_data['cards']

    first_name = update.message.chat.first_name if update.message.chat.first_name is not None else ''
    last_name = update.message.chat.last_name if update.message.chat.last_name is not None else ''
    username = update.message.chat.username
    telegram_id = update.effective_user.id

    if len(cards) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="شماره کارتی برای ساخت استیکر وارد نکردی😔")
        return CHOOSING
    if name is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="اسم برای ساخت استیکر وارد نکردی😔")
        return CHOOSING

    sticker_set_unique_name = update.effective_user.id
    update.message.reply_text("در حال ساخت پک استیکر...", reply_markup=ReplyKeyboardRemove())

    try:
        sticker_set = context.bot.getStickerSet(name=f'cc_{sticker_set_unique_name}_by_credit_card_sticker_bot')
    except error.TelegramError:
        sticker_set = None

    if sticker_set is not None:
        # delete stickers in pack and create new one
        for sticker in sticker_set.stickers:
            context.bot.delete_sticker_from_set(sticker=sticker.file_id)
        start_index = 0
    else:
        # create sticker set and add sticker to it from png file
        image = cc_renderer(name, cards[0])
        context.bot.create_new_sticker_set(user_id=update.effective_chat.id,
                                           name=f'cc_{sticker_set_unique_name}_by_credit_card_sticker_bot',
                                           title='credit card sticker set',
                                           png_sticker=image.getvalue(),
                                           emojis='💳')
        image.close()
        start_index = 1

    for card in cards[start_index:]:
        image = cc_renderer(name, card)
        context.bot.add_sticker_to_set(user_id=update.effective_chat.id,
                                       name=f'cc_{sticker_set_unique_name}_by_credit_card_sticker_bot',
                                       png_sticker=image.getvalue(),
                                       emojis='💳')
        image.close()

    # add ad sticker to set
    context.bot.add_sticker_to_set(user_id=update.effective_chat.id,
                                   name=f'cc_{sticker_set_unique_name}_by_credit_card_sticker_bot',
                                   png_sticker=config('AD_STICKER_FILE_ID'),
                                   emojis='💳')

    # send created sticker set to user
    sticker_set = context.bot.getStickerSet(name=f'cc_{sticker_set_unique_name}_by_credit_card_sticker_bot')
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=sticker_set.stickers[0])

    # log sticker set creation
    logger.info(f'{first_name} {last_name} with username {username} and id {telegram_id} created sticker set')
    context.bot.send_sticker(chat_id=config('CHANNEL_ID'), sticker=sticker_set.stickers[0], disable_notification=True)

    context.user_data.clear()
    return ConversationHandler.END


def about(update: Update, context: CallbackContext):
    about_message = f"""
خوشحال میشم اگر در راستای بهتر شدنم پیشنهادات رو به @SadjadEb بگی.
همچنین اگر بانکی تشخیص داده نمیشه هم میتونی اطلاع رسانی کنی تا اضافه بشه.
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=about_message)


def raw_text(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="اول باید انتخاب کنی چه اطلاعاتی رو قراره به من بدی🙄")


def sent_sticker(update: Update, context: CallbackContext):
    print(update.message.sticker.file_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="من خودم ذغال فروشم به من ذغال نده😁")


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ببخشید من این دستوری که زدی رو نمیفهمم🥲")


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('create', create)],
    states={
        CHOOSING: [
            MessageHandler(
                Filters.regex('^(وارد کردن اسم|وارد کردن شماره کارت)$'), regular_choice
            )
        ],
        TYPING_CHOICE: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex('^ساخت پک استیکر$')), regular_choice
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                Filters.text & ~(Filters.command | Filters.regex('^ساخت پک استیکر$')),
                received_information,
            )
        ],
    },
    fallbacks=[MessageHandler(Filters.regex('^ساخت پک استیکر$'), create_cc_sticker_set)],
)

handler_objects = [
    CommandHandler('start', start),
    conv_handler,
    CommandHandler('about', about),
    MessageHandler(Filters.text & (~Filters.command), raw_text),
    MessageHandler(Filters.sticker, sent_sticker),
    MessageHandler(Filters.command, unknown),
]


def run_bot():
    for handler in handler_objects:
        updater.dispatcher.add_handler(handler)
    updater.start_polling()
    updater.idle()
