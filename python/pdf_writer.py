import reportlab.rl_config
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from svglib.svglib import svg2rlg

from config import config

reportlab.rl_config.warnOnMissingFontGlyphs = 0

print(A4)

DEFAULT_FONT_NAME = 'OsnovaPro'

pdfmetrics.registerFont(TTFont(DEFAULT_FONT_NAME, './fonts/OsnovaPro.ttf'))
pdfmetrics.registerFont(TTFont('EuclidFlex-Regular', './fonts/EuclidFlex-Regular.ttf'))


def create_multipage_pdf(filename, template, participants_list, trainer_names, training_name, date, place, quotes_offset, training_type):
    pdf_config = config[template] if template in config else config['default']
    mid_width = A4[0] / 2
    c = Canvas(filename, pagesize=A4, bottomup=1)
    for participant in participants_list:
        create_page(c, pdf_config, template, mid_width, participant, training_name, trainer_names, date, place, quotes_offset, training_type)
        c.showPage()

    c.save()


def set_font(c, pdf_config, font_size):
    font_name = pdf_config['font_name'] if 'font_name' in pdf_config else DEFAULT_FONT_NAME
    c.setFont(font_name, font_size)


def draw_quotes(c, pdf_config, quotes_offset):
    """
    Width and height of svg images are hardcoded inside images themselves
    """
    quote_y = int(pdf_config['quote_y'])
    right_quote_x = int(pdf_config['right_quote_x'])
    left_quote_x = int(pdf_config['left_quote_x'])
    quote_l = svg2rlg('./images/quote_l.svg')
    quote_r = svg2rlg('./images/quote_r.svg')
    quote_l.drawOn(c, left_quote_x + quotes_offset, quote_y)
    quote_r.drawOn(c, right_quote_x - quotes_offset, quote_y)


def draw_logo(c, pdf_config, mid_width):
    """
    Width and height of svg are hardcoded inside svg itself
    However, logo width is used to center the image so it's also written in the config
    """
    logo_width = int(pdf_config['logo_width'])
    logo_y = int(pdf_config['logo_y'])
    logo_x = int(mid_width - logo_width / 2)
    d = svg2rlg('./images/logo.svg')
    d.drawOn(c, logo_x, logo_y)


def create_page(c, pdf_config, template, mid_width, trainee_name, training_name, trainer_names, date, place, quotes_offset, training_type):
    draw_background(c, template, mid_width, pdf_config, quotes_offset)
    print_supplementary_text(c, pdf_config, mid_width, training_type)
    print_trainee_name(c, pdf_config, mid_width, trainee_name)
    print_training_title(c, pdf_config, mid_width, training_name)
    print_date_and_place(c, pdf_config, mid_width, date, place)
    print_trainer_names(c, pdf_config, trainer_names)


def get_background_image(template):
    if template == 'TheSales':
        return 'images/TheSales_bg.png'
    else:
        return None


def draw_background(c, template, mid_width, pdf_config, quotes_offset):
    background = get_background_image(template)
    if background is not None:
        c.drawImage(background, x=0, y=0, width=A4[0], height=A4[1])
    else:
        draw_logo(c, pdf_config, mid_width)
        draw_quotes(c, pdf_config, quotes_offset)


def print_supplementary_text(c, pdf_config, mid_width, training_type):
    r = int(pdf_config['blue_color_r'])
    g = int(pdf_config['blue_color_g'])
    b = int(pdf_config['blue_color_b'])
    font_size = int(pdf_config['supplementary_font_size'])
    first_line_y = int(pdf_config['supplementary_first_line_y'])
    second_line_y = int(pdf_config['supplementary_second_line_y'])
    training_type_text = 'прошёл(-ла) тренинг' if training_type == 'training' else 'прошёл(-ла) мастер-класс'

    set_font(c, pdf_config, font_size)
    c.setFillColorRGB(r / 256, g / 256, b / 256)
    c.drawCentredString(mid_width, first_line_y, 'подтверждает, что')
    c.drawCentredString(mid_width, second_line_y, training_type_text)


def print_trainee_name(c, pdf_config, mid_width, trainee_name):
    font_size = int(pdf_config['trainee_font_size'])
    text_y = int(pdf_config['trainee_line_y'])

    set_font(c, pdf_config, font_size)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    c.drawCentredString(mid_width, text_y, trainee_name)


def print_training_title(c, pdf_config, mid_width, training_title):
    font_size = int(pdf_config['training_font_size'])
    text_mid_y = int(pdf_config['training_mid_y'])
    line_height = int(pdf_config['training_line_height'])

    set_font(c, pdf_config, font_size)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    training_name_lines = [l.strip() for l in training_title.split('\n') if l.strip() != '']
    start_top = text_mid_y + (len(training_name_lines) - 1) / 2 * line_height
    line_top = start_top
    for line in training_name_lines:
        c.drawCentredString(mid_width, line_top, line)
        line_top -= line_height


def print_date_and_place(c, pdf_config, mid_width, date, place):
    font_size = int(pdf_config['training_place_date_font_size'])
    text_y = int(pdf_config['training_place_date_y'])
    line_height = int(pdf_config['training_place_date_line_height'])
    set_font(c, pdf_config, font_size)
    c.drawCentredString(mid_width, text_y, date)
    c.drawCentredString(mid_width, text_y - line_height, place)


def print_trainer_names(c, pdf_config, trainer_names):
    font_size = int(pdf_config['trainer_font_size'])
    left = int(pdf_config['trainer_line_x'])
    top = int(pdf_config['trainer_line_y'])
    line_height = int(pdf_config['trainer_line_height'])
    signature_line_gap = int(pdf_config['trainer_signature_line_gap'])
    signature_line_length = int(pdf_config['trainer_signature_line_length'])

    set_font(c, pdf_config, font_size)
    trainer_names_list = [l.strip() for l in trainer_names.split('\n') if l.strip() != '']
    trainer_text =\
        pdf_config['trainer_text_single'] if len(trainer_names_list) == 1 else pdf_config['trainer_text_plural']
    c.drawString(left, top, trainer_text)
    second_line_y = top - line_height
    line_x_list = []
    for trainer_name in trainer_names_list:
        t = c.beginText(left, second_line_y)
        t.textOut(trainer_name)
        new_x, _ = t.getCursor()
        line_x_list.append(new_x)
        c.drawText(t)
        second_line_y -= line_height

    second_line_y = top - line_height
    max_x = max(line_x_list)
    for i, _ in enumerate(line_x_list):
        signature_line_x = max_x + signature_line_gap
        p = c.beginPath()
        p.moveTo(signature_line_x, second_line_y - 0.2)
        p.lineTo(signature_line_x + signature_line_length, second_line_y + 0.2)
        c.setLineWidth(0.5)
        c.drawPath(p)
        second_line_y -= line_height
