import reportlab.rl_config
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

reportlab.rl_config.warnOnMissingFontGlyphs = 0

pdfmetrics.registerFont(TTFont('OsnovaPro', 'OsnovaPro.ttf'))
pdfmetrics.registerFont(TTFont('OsnovaProLight', 'OsnovaProLight.ttf'))


def create_pdf(filename, trainee_name, trainer_name, training_name, date, place):
    mid_width = A4[0] / 2
    c = Canvas(filename, pagesize=A4, bottomup=0)
    c.setFont('OsnovaProLight', 22)
    c.setFillColorRGB(61 / 256, 189 / 256, 237 / 256)
    c.setFontSize(14)
    c.drawCentredString(mid_width, 275, 'подтверждает, что')
    c.drawCentredString(mid_width, 340, 'прошёл (-ла) обучение на тренинге')
    c.setFillColorRGB(0.0, 0.0, 0.0)
    c.setFont('OsnovaPro', 22)
    c.setFontSize(24)
    c.drawCentredString(mid_width, 311, trainee_name)
    c.setFontSize(18)
    training_name_lines = [l.strip() for l in training_name.split('\n') if l.strip() != '']
    start_top = 419 - (len(training_name_lines) - 1) / 2 * 30
    line_top = start_top
    for line in training_name_lines:
        c.drawCentredString(mid_width, line_top, line)
        line_top += 30

    top = 700
    c.setFontSize(11)
    c.drawCentredString(mid_width, top, date)
    c.drawCentredString(mid_width, top + 22, place)

    c.setFont('OsnovaProLight', 11)
    top = 567
    left = 96
    c.drawString(left, top, 'Бизнес-тренер:')
    t = c.beginText(left, top + 22)
    t.textOut(trainer_name)
    new_x, _ = t.getCursor()
    c.drawText(t)
    p = c.beginPath()
    p.moveTo(new_x + 8, top + 22.2)
    p.lineTo(new_x + 110, top + 22.2)
    c.setLineWidth(0.5)
    c.drawPath(p)

    c.save()
