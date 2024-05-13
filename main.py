import os
from multiprocessing import Process
from time import sleep
from lib import web
from lib import web_gradio
import signal

_host = os.environ.get('NN_SERVER', '127.0.0.1')
_port1 = int(os.environ.get('NN_PORT1', '5000'))
_port2 = int(os.environ.get('NN_PORT2', '5001'))

t1 = None
t2 = None

def on_sigterm(signum, frame):
    global t1, t2
    print('On sigterm')
    if t1 is not None:
        t1.terminate()
    if t2 is not None:
        t2.terminate()
    raise SystemExit(1)

signal.signal(signal.SIGTERM, on_sigterm)


t1 = Process(target=lambda: web_gradio.run_server(_host, _port1, _port2))
t2 = Process(target=lambda: web.run_flask(_host, _port1))

print('Starting gradio')
t1.start()
print('Starting flask')
t2.start()

try:
    t1.join()
finally: ...
try:
    t2.join()
finally: ...

#LectureParser('./input/1.mkv', './output/1.mp3', './output/1_result.docx').run()
#LectureParser('./input/2.webm', './output/2.mp3', './output/2_result.docx').run()
#LectureParser('./input/3.mkv', './output/3.mp3', './output/3_result.docx').run()


