import os.path
import pickle
import threading
from datetime import datetime
from functools import partial
from time import sleep
from .parser import LectureParser
from .constants import *

class Controller:

    def __init__(self, instance, absolute_path=False):
        self.instance = instance
        self.absolute_path = absolute_path
        self.pickle_name = f'{self.instance}_tasks.pickle'
        self._tasks = []
        if os.path.isfile(self.pickle_name):
            self.pickle_load()
        threading.Thread(target=self.processor_thread).start()
        self.lock = threading.Lock()

    def add_task(self, filename, status, result, storage_name):
        task_id = int(datetime.timestamp(datetime.now())*1000)
        with self.lock:
            self._tasks.append(
                {
                  'id': task_id,
                  'filename': filename,
                  'storage_name': storage_name,
                  'status': status,
                  'result': result}
            )
            self.pickle_save()
        return task_id


    def get_tasks(self):
        return self._tasks


    def pickle_save(self):
        with open(self.pickle_name, 'wb') as f:
            pickle.dump(self._tasks, f)

    def pickle_load(self):
        with open(self.pickle_name, 'rb') as f:
            self._tasks = pickle.load(f)
        for t in filter(lambda x: x['status'] not in {'NEW', 'DONE'}, self._tasks):
            t['status'] = 'CANCELED'
        self.pickle_save()

    def delete_task(self, task_id):
        with self.lock:
            task_to_delete = next(filter(lambda x: str(x['id']) == task_id, self._tasks))
            in_file_name = INPUT_FOLDER + task_to_delete['storage_name'] if not self.absolute_path else task_to_delete['storage_name']
            if os.path.isfile(in_file_name):
                os.remove(in_file_name)
            out_file_name = OUTPUT_FOLDER + task_to_delete['storage_name']+'.docx' if not self.absolute_path else task_to_delete['storage_name']+'.docx'
            if os.path.isfile(out_file_name):
                os.remove(out_file_name)
            self._tasks = list(filter(lambda x: str(x['id']) != task_id, self._tasks))
            # print(self._tasks)
            self.pickle_save()

    def processor_thread(self):
        def save_status(task_item, status):
            print('Status changed', status)
            with self.lock:
                task_item['status'] = status
                self.pickle_save()
        while True:
            sleep(1)
            with self.lock:
                try:
                    task = next(filter(lambda x: x['status'] == 'NEW', self._tasks))
                except StopIteration:
                    continue
                task['status'] = 'PROCESSING'
                self.pickle_save()
            print('Processing task')
            in_file = INPUT_FOLDER + task['storage_name'] if not self.absolute_path else task['storage_name']
            out_file = OUTPUT_FOLDER + task['storage_name']+'.docx' if not self.absolute_path else task['storage_name']+'.docx'
            #print(task)
            status_partial = partial(save_status, task)
            status_partial('TESTING')
            try:
                LectureParser(in_file, out_file, status_partial).run()
                with self.lock:
                    task['result'] = task['filename'] + '.docx'
                    self.pickle_save()
            except Exception as e:
                print('Exception: ', str(e))
                with self.lock:
                    task['status'] = 'ERROR'
                    self.pickle_save()

    def get_download_file_name(self, task_id):
        task = next(filter(lambda x: str(x['id']) == task_id, self._tasks))
        return OUTPUT_FOLDER + task['storage_name']+'.docx' if not self.absolute_path else task['storage_name']+'.docx'

    def wait_for_task(self, task_id):
        while True:
            task = next(filter(lambda x: x['id'] == task_id, self._tasks))
            if task['status'] == 'DONE':
                return True
            elif task['status'] == 'ERROR' or task['status'] == 'CANCELED':
                return False
            sleep(1)

#controller = Controller()
