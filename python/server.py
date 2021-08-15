import io

from flask import Flask, render_template, request, send_file
from pdf_writer import create_multipage_pdf

app = Flask(__name__, template_folder='../templates/', static_url_path='/static', static_folder='../static')


@app.route('/')
def serve_main():
    return render_template('main.html')


def parse_int(string_value, default_value):
    try:
        return int(string_value)
    except ValueError:
        return default_value


@app.route('/generate', methods=['POST'])
def generate():
    training_name = request.form['training_name']
    trainer_name = request.form['trainer_name']
    training_date = request.form['training_date']
    training_place = request.form['training_place']
    quotes_offset = parse_int(request.form['quotes_offset'], 0)
    training_type = request.form['training_type']
    participants = request.form['participants']
    participants_list = [p.strip() for p in participants.split('\n')]
    print('Generating PDF for `{}`, {} participants'
          .format(training_name.replace('\n', ' ').replace('\r', ''), len(participants_list)))

    buffer = io.BytesIO()
    create_multipage_pdf(
        buffer, participants_list, trainer_name, training_name, training_date, training_place, quotes_offset, training_type)
    formatted_date = training_date.replace(' ', '_')
    buffer.seek(0)
    return send_file(buffer, 'application/pdf', True, 'Тренинг-{}-{}.pdf'.format(formatted_date, trainer_name))
