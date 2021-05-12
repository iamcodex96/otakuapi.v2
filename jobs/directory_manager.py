import threading, time, datetime, os, shutil


class Worker(threading.Thread):
    def __init__(self, thread_name, thread_ID, seconds):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.delay = seconds
        self.is_done = False
        self.job = None

    def done(self):
        self.is_done = True

    def run(self):
        while not self.is_done:
            if self.job is not None:
                self.job()
            else:
                print('No job assigned')
                self.is_done = True
            time.sleep(self.delay)
        print('The Job is Done')

    def assign_job(self, job):
        self.job = job


class DirectoryManager:
    def __init__(self, time, directory, file_life_span):
        self.time = time
        self.directory = directory
        self._worker = Worker('Directory Manager', 2525, time)
        self.file_life_span = file_life_span

    def start(self):
        self.define_worker_job()
        self._worker.start()

    def define_worker_job(self):
        self._worker.assign_job(self.directory_checker)

    def directory_checker(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/temp/manga/'
        mangas_downloaded = os.listdir(base_path)
        for manga in mangas_downloaded:
            print(f'CREATED AT : {os.stat(f"{base_path}/{manga}").st_ctime}')
            time_adder = datetime.timedelta(minutes=self.file_life_span)
            file_create_time = datetime.datetime.fromtimestamp(os.stat(f"{base_path}/{manga}").st_ctime)
            life_span_end = file_create_time + time_adder
            if datetime.datetime.now() > life_span_end:
                shutil.rmtree(f"{base_path}/{manga}")
                print(f'Manga : {manga} - is old [ HAS BEEN DELETED ]')
            else:
                print(f'Manga : {manga} - is recent')
        print(f'CHECKING DIRECTORIES... ON {self.directory}')
