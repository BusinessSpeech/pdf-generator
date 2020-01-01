import os

from pdf_writer import create_pdf
from zip_creation import create_zip
from flask import Flask, url_for, render_template, request, send_file
from temp_dir_util import create_temp_dir, delete_temp_dir
app = Flask(__name__, template_folder='templates/')


@app.route('/')
def serve_main():
    return render_template('main.html')


@app.route('/generate', methods=['POST'])
def generate():
    training_name = request.form['training_name']
    trainer_name = request.form['trainer_name']
    training_date = request.form['training_date']
    training_place = request.form['training_place']
    participants = request.form['participants']
    participants_list = [p.strip() for p in participants.split('\n') if p.strip() != '']
    print(len(participants_list))
    temp_dir_name = create_temp_dir()
    for participant in participants_list:
        filename = participant.replace(' ', '_')
        create_pdf(os.path.join(temp_dir_name, '{}.pdf'.format(filename)), participant, trainer_name, training_name,
                   training_date, training_place)
    zip_file_name = create_zip(temp_dir_name)
    formatted_date = training_date.replace(' ', '_')
    delete_temp_dir(temp_dir_name)
    return send_file(zip_file_name, 'application/zip', True, 'Тренинг-{}.zip'.format(formatted_date))
