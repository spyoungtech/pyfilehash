import argparse
from hashlib import md5, sha1, sha224, sha256, sha384
import os

import easygui as eg

parser = argparse.ArgumentParser()
parser.add_argument("algorithm")
parser.add_argument("path")
args = parser.parse_args()

hash_dict = {"md5": md5,
             "sha1": sha1,
             "sha224": sha224,
             "sha256": sha256,
             "sha384": sha384}

if args.algorithm.lower() not in hash_dict:
    raise ValueError("Invalid algorithm '{}'".format(args.algorithm))

assert os.path.isfile(args.path)

hash_func = hash_dict[args.algorithm.lower()]

box = eg.buttonbox(msg="Loading...\nProgress: 0%", title="PyFileHash", choices=["Cancel"], cancel_choice="Cancel", run=False)
#icon_path = os.path.join(__file__, "icon.ico")
#box.ui.boxRoot.iconbitmap(icon_path)

class FileLoader(object):
    def __init__(self, fp):
        self.fp = fp
        self.file_size = os.stat(self.fp).st_size
        self.chunk_size = int(self.file_size / 20)+1
        self.file = open(self.fp, 'rb')
        self.progress = 0
        self.data = b''
        self.progress_incr = 100 / (self.file_size / self.chunk_size)
        self.reader = self.chunk_reader()
    def chunk_reader(self):
        while True:
            next_data = self.file.read(self.chunk_size)
            if next_data:
                self.progress += self.progress_incr
                self.data += next_data
                box.msg = "Loading...\nProgress: {}%".format(int(self.progress))
                yield next_data
            else:
                box.msg = "Complete!"
                break
    def read(self):
        try:
            next_chunk = next(self.reader)
            box.ui.boxRoot.after(0, self.read())
        except StopIteration:
            try:
                box.ui.boxRoot.destroy()
            except:
                pass



f = FileLoader(args.path)
box.ui.boxRoot.after(0, f.read())
try:
    box.run()
except:
    pass

result = hash_func(f.data).hexdigest()

message = """Results for {}:
{}: {}
""".format(os.path.abspath(args.path), args.algorithm.upper(), result)

eg.msgbox(msg=message, title="PyFileHash")