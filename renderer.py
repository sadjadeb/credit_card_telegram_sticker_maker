from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from banks_data import banks


def hyphenate_card_number(card_number: str):
    hyphenated = '-'.join(card_number[i: i + 4] for i in range(0, len(card_number), 4))
    return hyphenated


def get_bank_name(card_number):
    for bank in banks:
        if card_number[0:6] == str(bank['card_no']):
            return bank['bank_name']


def cc_renderer(name, card_number):
    if len(card_number) != 16:
        raise ValueError('Card number must be 16 digits long')

    # change card number from wwwwxxxxyyyyzzzz to wwww-xxxx-yyyy-zzzz
    hyphenated_card_number = hyphenate_card_number(card_number)
    # get bank name
    bank_name = get_bank_name(card_number)
    if bank_name is None:
        raise ValueError('Card number is not valid')

    # load the font and image
    font = ImageFont.truetype('fonts/BTitrBd.ttf', 30)
    image = Image.open(f'base_images/{bank_name}.png')
    base_width, base_height = image.size

    # correct text shape for persian
    reshaped_text = get_display(arabic_reshaper.reshape(name))
    reshaped_number = get_display(arabic_reshaper.reshape(hyphenated_card_number))

    # start drawing on image
    draw = ImageDraw.Draw(image)
    width = (base_width - draw.textsize(reshaped_number, font=font)[0]) / 2
    draw.text((width, 345), reshaped_number, fill="black", font=font)
    width = (base_width - draw.textsize(reshaped_text, font=font)[0]) / 2
    draw.text((width, 443), reshaped_text, fill="black", font=font)

    image.show()

    # image.save("output.png")
