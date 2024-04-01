import os
import uuid
from flask import Flask, render_template, send_from_directory, request, redirect
from .controller import controller
from .constants import OUTPUT_FOLDER
app = Flask(__name__)

@app.route('/style.css')
def style():
    return send_from_directory('templates', 'style.css')

@app.route('/')
def index():
    tasks = controller.get_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/delete_task', methods=['POST'])
def delete_task():
    print(dict(request.form))
    task_id = request.form['task_id']
    controller.delete_task(task_id)
    return 'OK'

@app.route('/upload_file', methods=['POST'])
def upload_file():
    print(dict(request.form))
    file = request.files['file']
    storage_name = str(uuid.uuid4())
    file.save('./input/' + storage_name)
    controller.add_task(file.filename, 'NEW', None, storage_name)
    print(controller._tasks)
    return redirect("/", code=302)

@app.route('/download_file/<task_id>', methods=['GET'])
def download_file(task_id):
    print(task_id)
    filename = controller.get_download_file_name(task_id)[len(OUTPUT_FOLDER):]
    #uploads = os.path.join(app.root_path, OUTPUT_FOLDER[2:])
    #print(uploads, filename, app.root_path, OUTPUT_FOLDER[2:])
    return send_from_directory('..'+OUTPUT_FOLDER[1:], filename)

