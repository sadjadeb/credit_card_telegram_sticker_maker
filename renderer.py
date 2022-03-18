from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from banks_data import banks


def hyphenate_card_number(card_number: str):
    hyphenated = '-'.join(card_number[i: i + 4] for i in range(0, len(card_number), 4))
    return hyphenated


def get_bank(card_number):
    for bank in banks:
        if card_number[0:6] == str(bank['card_no']):
            return bank


def cc_renderer(name, card_number):
    if len(card_number) != 16:
        raise ValueError('Card number must be 16 digits long')

    # change card number from wwwwxxxxyyyyzzzz to wwww-xxxx-yyyy-zzzz
    hyphenated_card_number = hyphenate_card_number(card_number)
    # get bank name
    bank = get_bank(card_number)
    if bank is None:
        raise ValueError('Card number is not valid')

    # load the font and image
    font = ImageFont.truetype('fonts/BTitrBd.ttf', 30)
    # create 430x512 image as base
    base_width, base_height = 430, 512
    base_image = Image.new('RGB', (base_width, base_height), 0)
    base_image.putalpha(0)

    # correct text shape for persian
    reshaped_text = get_display(arabic_reshaper.reshape(name))
    reshaped_number = get_display(arabic_reshaper.reshape(hyphenated_card_number))

    # start drawing on image
    draw = ImageDraw.Draw(base_image)

    # draw logo on image
    logo = Image.open(f'logos/{bank["bank_name"]}.png')
    base_image.paste(logo, (65, 5))

    # draw background
    draw.rounded_rectangle((12, 320, 416, 391), fill="white", outline=bank["color"], width=4, radius=30)
    draw.rounded_rectangle((87, 425, 341, 486), fill="white", outline=bank["color"], width=4, radius=30)

    # draw texts
    width = (base_width - draw.textsize(reshaped_number, font=font)[0]) / 2
    draw.text((width, 345), reshaped_number, fill="black", font=font)
    width = (base_width - draw.textsize(reshaped_text, font=font)[0]) / 2
    draw.text((width, 443), reshaped_text, fill="black", font=font)

    base_image.show()

    # image.save("output.png")
