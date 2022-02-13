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
    template = request.form['template']
    training_name = request.form['training_name']
    trainer_names = request.form['trainer_names']
    training_date = request.form['training_date']
    training_place = request.form['training_place']
    quotes_offset = parse_int(request.form['quotes_offset'], 0)
    training_type = request.form['training_type']
    participants = request.form['participants']
    signature_file_names = [f'sign{i}' for i in range(1, 4)]
    signatures = [
        io.BytesIO(request.files[name].read()) for name in signature_file_names if
        (name in request.files and request.files[name].filename != '')
    ]
    participants_list = [p.strip() for p in participants.split('\n')]
    print('Generating PDF for `{}`, {} participant(s)'
          .format(training_name.replace('\n', ' ').replace('\r', ''), len(participants_list)))

    buffer = io.BytesIO()
    create_multipage_pdf(buffer, template, participants_list, trainer_names, signatures, training_name, training_date,
                         training_place, quotes_offset, training_type)
    formatted_date = training_date.replace(' ', '_')
    buffer.seek(0)
    trainers_string = '-'.join(trainer_names.split('\n')).replace('\r', '')
    return send_file(buffer, 'application/pdf', True, 'Тренинг-{}-{}.pdf'.format(formatted_date, trainers_string))
