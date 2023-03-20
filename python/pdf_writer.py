from itertools import zip_longest
from typing import List

import reportlab.rl_config
from reportlab.lib.pagesizes import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from svglib.svglib import svg2rlg

from config import select_config

reportlab.rl_config.warnOnMissingFontGlyphs = 0

DEFAULT_FONT_NAME = 'OsnovaPro'
PAGE_SIZE = (216*mm, 303*mm)

pdfmetrics.registerFont(TTFont(DEFAULT_FONT_NAME, './fonts/OsnovaPro.ttf'))
pdfmetrics.registerFont(TTFont('EuclidFlex-Regular', './fonts/EuclidFlex-Regular.ttf'))


def get_next_number(number):
    return None if number is None else number + 1


def create_multipage_pdf(filename, template, participants_list, trainer_names, trainer_signatures, training_name, date,
                         place, quotes_offset, training_type_text, first_cert_number):
    c = Canvas(filename, pagesize=PAGE_SIZE, bottomup=1)
    number = first_cert_number
    for participant in participants_list:
        create_page(c, template, PAGE_SIZE, participant, training_name, trainer_names, trainer_signatures, date, place,
                    quotes_offset, training_type_text, number)
        number = get_next_number(number)
        c.showPage()

    c.save()


def create_single_pdf(file_object, template, participant, trainer_names, trainer_signatures, training_name, date,
                      place, quotes_offset, training_type, cert_number):
    c = Canvas(file_object, pagesize=PAGE_SIZE, bottomup=1)
    create_page(c, template, PAGE_SIZE, participant, training_name, trainer_names, trainer_signatures, date, place, quotes_offset,
                training_type, cert_number)
    c.showPage()
    c.save()


def draw_quotes(c, quotes_config, quotes_offset):
    """
    Width and height of svg images are hardcoded inside images themselves
    """
    quote_y = int(quotes_config['y'])
    right_quote_x = int(quotes_config['right_x'])
    left_quote_x = int(quotes_config['left_x'])
    quote_l = svg2rlg('./images/quote_l.svg')
    quote_r = svg2rlg('./images/quote_r.svg')
    quote_l.drawOn(c, left_quote_x + quotes_offset, quote_y)
    quote_r.drawOn(c, right_quote_x - quotes_offset, quote_y)


def create_page(c, template, document_size, trainee_name, training_name, trainer_names, trainer_signatures, date, place, quotes_offset,
                training_type_text, cert_number):
    current_config = select_config(template)
    middle = document_size[0] / 2
    draw_background(c, current_config, document_size)
    print_trainee_name(c, current_config, middle, trainee_name)
    print_training_title(c, current_config, middle, training_name)
    print_date_and_place(c, current_config, middle, date, place)
    print_trainer_names(c, current_config, trainer_names, trainer_signatures)
    if cert_number is not None:
        print_certificate_number(c, cert_number, current_config, middle)

    if template == 'Business Speech':
        draw_quotes(c, current_config['quotes'], quotes_offset)
        print_supplementary_text(c, current_config, middle, 'подтверждает, что', training_type_text)
    elif template == 'TheSales':
        draw_text_by_config(c, ['www.thesales.ru'], middle, current_config['defaults'], current_config['site'])
        print_supplementary_text(c, current_config, middle, 'подтверждает, что', training_type_text)
    elif template == 'SCT':
        print_supplementary_text(
            c, current_config, middle, 'Настоящий сертификат подтверждает, что', training_type_text
        )


def get_or_default(key, specific_config, default_config):
    return specific_config[key] if key in specific_config else default_config[key]


def draw_text_by_config(c, lines: List[str], middle, defaults, text_config):
    set_font(c, text_config, defaults)
    lines_count = len(lines)
    y = int(text_config['y'])
    x = int(text_config['x']) if 'x' in text_config else None
    lh = int(text_config['line_height']) if 'line_height' in text_config else 0
    first_line_y = y if 'align_top' in text_config else centered_text_first_line_y(y, lh, lines_count)
    for i, line in enumerate(lines):
        text_y = first_line_y - lh * i
        if x is None:
            c.drawCentredString(middle, text_y, line)
        else:
            c.drawString(x, text_y, line)


def centered_text_first_line_y(y, line_height, lines_count):
    return y + line_height / 2 * (lines_count - 1)


def set_font(c, text_config, defaults):
    font_name = get_or_default('font_name', text_config, defaults)
    font_size = int(get_or_default('font_size', text_config, defaults))
    color_r = int(get_or_default('color_r', text_config, defaults))
    color_g = int(get_or_default('color_g', text_config, defaults))
    color_b = int(get_or_default('color_b', text_config, defaults))
    c.setFont(font_name, font_size)
    c.setFillColorRGB(color_r / 256, color_g / 256, color_b / 256)


def split_by_newlines(text: str) -> List[str]:
    return [line.strip() for line in text.split('\n') if line.strip() != '']


def draw_background(c, current_config, document_size):
    background = 'images/' + current_config['background']['image_name']
    c.drawImage(background, x=0, y=0, width=document_size[0], height=document_size[1])


def print_supplementary_text(c, current_config, middle, prefix, training_type_text):
    draw_text_by_config(
        c, [prefix, training_type_text], middle,
        current_config['defaults'], current_config['supplementary']
    )


def print_trainee_name(c, current_config, middle, trainee_name):
    draw_text_by_config(c, [trainee_name], middle, current_config['defaults'], current_config['trainee'])


def print_training_title(c, current_config, middle, training_name):
    training_name_lines = split_by_newlines(training_name)
    draw_text_by_config(c, training_name_lines, middle, current_config['defaults'], current_config['training'])


def print_date_and_place(c, current_config, middle, date, place):
    draw_text_by_config(c, [date, place], middle, current_config['defaults'], current_config['date_place'])


def print_trainer_names(c, current_config, trainer_names, trainer_signatures):
    trainers_config = current_config['trainers']
    set_font(c, trainers_config, current_config['defaults'])
    trainer_names_list = split_by_newlines(trainer_names)
    trainer_text = trainers_config['text_single'] \
        if len(trainer_names_list) == 1 else trainers_config['text_plural']
    y = int(trainers_config['y'])
    line_height = int(trainers_config['line_height'])
    first_line_y = centered_text_first_line_y(y, line_height, len(trainer_names_list) + 1)
    do_print_trainer_names(
        c, int(trainers_config['x']), first_line_y, line_height,
        int(trainers_config['signature_line_gap']), int(trainers_config['signature_line_length']),
        trainer_names_list, trainer_signatures, trainer_text
    )


def do_print_trainer_names(c, x, y, line_height, signature_line_gap, signature_line_length, trainer_names_list,
                           trainer_signatures, trainer_text):
    c.drawString(x, y, trainer_text)
    second_line_y = y - line_height
    line_x_list = []
    for trainer_name in trainer_names_list:
        t = c.beginText(x, second_line_y)
        t.textOut(trainer_name)
        new_x, _ = t.getCursor()
        line_x_list.append(new_x)
        c.drawText(t)
        second_line_y -= line_height

    second_line_y = y - line_height
    max_x = max(line_x_list)
    for _, trainer_signature in zip_longest(trainer_names_list, trainer_signatures):
        signature_line_x = max_x + signature_line_gap
        p = c.beginPath()
        p.moveTo(signature_line_x, second_line_y - 0.2)
        p.lineTo(signature_line_x + signature_line_length, second_line_y + 0.2)
        c.setLineWidth(0.5)
        c.drawPath(p)
        if trainer_signature is not None:
            reader = ImageReader(trainer_signature)
            sign_size = reader.getSize()
            sign_height = line_height * 3
            sign_dx = 5
            sign_dy = sign_height / 2
            sign_scale = sign_size[1] / sign_height
            sign_width = int(sign_size[0] / sign_scale)
            c.drawImage(reader, x=signature_line_x + sign_dx, y=second_line_y - sign_dy,
                        width=sign_width, height=sign_height, mask=[255, 255, 255, 255, 255, 255])
        second_line_y -= line_height


def resolve_training_type_text(training_type, training_type_string):
    if training_type_string is not None and training_type_string != '':
        return training_type_string
    return 'прошёл(-ла) тренинг' if training_type == 'training' else 'прошёл(-ла) мастер-класс'


def print_certificate_number(c, number, current_config, middle):
    certificate_number_config = current_config['certificate_number']
    defaults = current_config['defaults']
    draw_text_by_config(c, ['№ ' + str(number)], middle, defaults, certificate_number_config)
