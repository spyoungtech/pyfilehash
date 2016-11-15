import easygui as eg
import os
from hashlib import md5, sha1, sha224, sha256, sha384

PROGRESS = 0

box = eg.buttonbox(msg="Progress... {}%".format(PROGRESS), choices=["Cancel"], cancel_choice="Cancel", run=False)
box.ui.boxRoot.iconbitmap(r'C:\Python27\Lib\site-packages\easygui-0.97.4-py2.7.egg\easygui\favicon.ico')

class FileLoader(object):
    def __init__(self, fp, chunk_size=None):
        self.fp = fp
        self.file_size = os.stat(self.fp).st_size
        if chunk_size:
            self.chunk_size = chunk_size
        else:
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
                box.msg = "Progress... {}%".format(int(self.progress))
                yield next_data
            else:
                box.msg = "Complete!"
                break
    def read(self):
        try:
            next_chunk = next(self.reader)
            #self.data += next_chunk
            box.ui.boxRoot.after(0, self.read())
        except StopIteration:
            #box.ui.boxRoot.after(0, box.stop)
            #box.ui._choices.append("MD5")
            #box.ui.create_buttons(box.ui._choices, box.ui._default_choice)
            return None


#h_dict = {"MD5": md5}

f = FileLoader("allitems.xml")
box.ui.boxRoot.after(100, f.read())
#hash_choice = box.run()
#hash_func = h_dict[hash_choice]
#result = hash_func(f.data).hexdigest()

try:
    box.run()
except AttributeError:
    pass


eg.msgbox(msg=result)
print(result)