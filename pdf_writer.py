import reportlab.rl_config
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from config import config

reportlab.rl_config.warnOnMissingFontGlyphs = 0

FONT_NAME = 'OsnovaPro'
FONT_NAME_LIGHT = 'OsnovaProLight'

pdfmetrics.registerFont(TTFont(FONT_NAME, 'OsnovaPro.ttf'))
pdfmetrics.registerFont(TTFont(FONT_NAME_LIGHT, 'OsnovaProLight.ttf'))


def create_pdf(filename, trainee_name, trainer_name, training_name, date, place):
    pdf_config = config['pdf'] if 'pdf' in config else dict()
    mid_width = A4[0] / 2
    c = Canvas(filename, pagesize=A4, bottomup=0)
    print_supplementary_text(c, pdf_config, mid_width)
    print_trainee_name(c, pdf_config, mid_width, trainee_name)
    print_training_title(c, pdf_config, mid_width, training_name)
    print_date_and_place(c, pdf_config, mid_width, date, place)
    print_trainer_name(c, pdf_config, trainer_name)

    c.save()


def print_supplementary_text(c, pdf_config, mid_width):
    r = int(pdf_config['blue_color_r'])
    g = int(pdf_config['blue_color_g'])
    b = int(pdf_config['blue_color_b'])
    font_size = int(pdf_config['supplementary_font_size'])
    first_line_y = int(pdf_config['supplementary_first_line_y'])
    second_line_y = int(pdf_config['supplementary_second_line_y'])

    c.setFont(FONT_NAME_LIGHT, font_size)
    c.setFillColorRGB(r / 256, g / 256, b / 256)
    c.drawCentredString(mid_width, first_line_y, 'подтверждает, что')
    c.drawCentredString(mid_width, second_line_y, 'прошёл (-ла) обучение на тренинге')


def print_trainee_name(c, pdf_config, mid_width, trainee_name):
    font_size = int(pdf_config['trainee_font_size'])
    text_y = int(pdf_config['trainee_line_y'])

    c.setFont(FONT_NAME, font_size)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    c.drawCentredString(mid_width, text_y, trainee_name)


def print_training_title(c, pdf_config, mid_width, training_title):
    font_size = int(pdf_config['training_font_size'])
    text_mid_y = int(pdf_config['training_mid_y'])
    line_height = int(pdf_config['training_line_height'])

    c.setFont(FONT_NAME, font_size)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    training_name_lines = [l.strip() for l in training_title.split('\n') if l.strip() != '']
    start_top = text_mid_y - (len(training_name_lines) - 1) / 2 * line_height
    line_top = start_top
    for line in training_name_lines:
        c.drawCentredString(mid_width, line_top, line)
        line_top += line_height


def print_date_and_place(c, pdf_config, mid_width, date, place):
    font_size = int(pdf_config['training_place_date_font_size'])
    text_y = int(pdf_config['training_place_date_y'])
    line_height = int(pdf_config['training_place_date_line_height'])
    c.setFont(FONT_NAME, font_size)
    c.drawCentredString(mid_width, text_y, date)
    c.drawCentredString(mid_width, text_y + line_height, place)


def print_trainer_name(c, pdf_config, trainer_name):
    font_size = int(pdf_config['trainer_font_size'])
    left = int(pdf_config['trainer_line_x'])
    top = int(pdf_config['trainer_line_y'])
    line_height = int(pdf_config['trainer_line_height'])
    signature_line_gap = int(pdf_config['trainer_signature_line_gap'])
    signature_line_length = int(pdf_config['trainer_signature_line_length'])

    c.setFont(FONT_NAME_LIGHT, font_size)
    c.drawString(left, top, 'Бизнес-тренер:')
    second_line_y = top + line_height
    t = c.beginText(left, second_line_y)
    t.textOut(trainer_name)
    new_x, _ = t.getCursor()
    c.drawText(t)

    signature_line_x = new_x + signature_line_gap
    p = c.beginPath()
    p.moveTo(signature_line_x, second_line_y + 0.2)
    p.lineTo(signature_line_x + signature_line_length, second_line_y + 0.2)
    c.setLineWidth(0.5)
    c.drawPath(p)
