import traceback
from time import sleep
from typing import List, Optional

import gradio as gr
from .controller import Controller
import os
running = False
controller: Optional[Controller] = None


def process_files(files: List[str]):
    result = []
    for f in files:
        task_id = controller.add_task(f, 'NEW', None, f)
        if controller.wait_for_task(task_id):
            result.append(f+'.docx')
    return result


def run_server(host, port_1, port_2):
    global controller
    controller = Controller('gradio', absolute_path=True)
    with gr.Blocks() as iface:
        gr.Markdown("""# File Uploader""")
        infile = gr.File(label='File to load', type='filepath', file_count='multiple')
        submit = gr.Button("Submit")
        outfile = gr.File(label='File to download', type='filepath', file_count='multiple')
        submit.click(fn=process_files, inputs=infile, outputs=outfile, api_name="greet")
        gr.Markdown(f'[Полноценный интерфейс](http://{host}:{port_1}/)')
    # Run the interface
    iface.launch(server_name=host, server_port=port_2)

