import io
import zipfile

from flask import Flask, render_template, request, send_file
from pdf_writer import create_multipage_pdf, create_single_pdf, resolve_training_type_text
from image_processor import make_transparent_pixels_white

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
    training_type_string = request.form['training_type_string']
    participants = request.form['participants']
    signature_file_names = [f'sign{i}' for i in range(1, 4)]
    signatures = [
        make_transparent_pixels_white(io.BytesIO(request.files[name].read())) for name in signature_file_names if
        (name in request.files and request.files[name].filename != '')
    ]
    effective_training_type_text = resolve_training_type_text(training_type, training_type_string)
    participants_list = [p.strip() for p in participants.split('\n')]
    separate_files = 'separate_files' in request.form
    print('Generating PDF for `{}`, {} participant(s)'
          .format(training_name.replace('\n', ' ').replace('\r', ''), len(participants_list)))

    buffer = io.BytesIO()
    if separate_files:
        print('Separate files requested')
        application_type = 'application/zip'
        file_extension = 'zip'
        with zipfile.ZipFile(buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for participant in participants_list:
                buf = io.BytesIO()
                create_single_pdf(buf, template, participant, trainer_names, signatures, training_name,
                                  training_date, training_place, quotes_offset, effective_training_type_text)
                buf.seek(0)
                participant_underscored = participant.replace(' ', '_')
                zf.writestr(f'{participant_underscored}.pdf', buf.read())
    else:
        print('Single pdf requested')
        application_type = 'application/pdf'
        file_extension = 'pdf'
        create_multipage_pdf(buffer, template, participants_list, trainer_names, signatures, training_name,
                             training_date, training_place, quotes_offset, effective_training_type_text)

    formatted_date = training_date.replace(' ', '_')
    buffer.seek(0)
    trainers_string = '-'.join(trainer_names.split('\n')).replace('\r', '')
    return send_file(buffer, application_type, True, 'Тренинг-{}-{}.{}'.format(formatted_date, trainers_string, file_extension))
