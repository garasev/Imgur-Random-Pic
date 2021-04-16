# This is a sample Python script.
import time

import requests
import random
import string
import os
import multiprocessing


CACHE_PATH = os.path.normpath(os.getcwd() + os.path.normpath('/cache'))
IMG_PATH = os.path.normpath(os.getcwd() + os.path.normpath('/img'))
INVALID_SIZE = [0, 503, 5296]

if not os.path.exists(CACHE_PATH):
    os.mkdir(CACHE_PATH)
if not os.path.exists(IMG_PATH):
    os.mkdir(IMG_PATH)
for char in string.digits + string.ascii_letters:
    name = CACHE_PATH + os.path.normpath('/.' + 'cache' + char)
    if not os.path.exists(name):
        os.mkdir(name)


class Scraper(multiprocessing.Process):
    def __init__(self, count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = count

    def run(self):
        if self.count is None:
            while True:
                self.get_pic()
        for _ in range(self.count):
            self.get_pic()

    def get_pic(self):
        base_url = 'https://i.imgur.com/'
        path = self.gen_path()
        tmp = ''
        if random.random() > 0.5:
            tmp = 'a/'
        p = requests.get(base_url + tmp + path + '.png')
        if self.check_cache(path):
            out = open(os.path.join(IMG_PATH, path + '.png'), "wb")
            out.write(p.content)
            out.close()
            if os.path.getsize(os.path.join(IMG_PATH, path + '.png')) in INVALID_SIZE:
                print('Invalid path:', path, flush=True)
                os.remove(os.path.join(IMG_PATH, path + '.png'))
            else:
                print('Valid path:', path, flush=True)
        else:
            print('Invalid path:', path, flush=True)
        time.sleep(1)

    @staticmethod
    def gen_path():
        length = random.randint(6, 7)

        if random.random() > 0.5:
            lst = string.ascii_letters + string.digits
        else:
            lst = string.ascii_letters

        return ''.join([random.choice(lst) for _ in range(length)])

    @staticmethod
    def check_cache(path):
        tmp = os.path.join(CACHE_PATH, '.cache' + path[0])
        files = os.listdir()
        if path in files:
            return False
        else:
            cache = open(os.path.join(tmp, path), "wb")
            cache.close()
            return True


if __name__ == '__main__':
    processes = []
    count = 10
    img = None
    for _ in range(count):
        tmp = Scraper(img)
        tmp.start()
        processes.append(tmp)

    for process in processes:
        process.join()
