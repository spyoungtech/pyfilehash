import argparse
from hashlib import md5, sha1, sha224, sha256, sha384, sha512
import os


parser = argparse.ArgumentParser()
parser.add_argument("algorithm", help="The algorithm to use, I.E MD5, SHA1, SHA256, etc.",)
parser.add_argument("path", help="The path of the file. Can be relative or absolute.")
parser.add_argument("-q", "--quiet", action="store_true", help="Quiet flag. Supresses GUI")
args = parser.parse_args()

hash_dict = {"md5": md5,
             "sha1": sha1,
             "sha224": sha224,
             "sha256": sha256,
             "sha384": sha384,
             "sha512": sha512}

if args.algorithm.lower() not in hash_dict:
    raise ValueError("Invalid algorithm '{}'".format(args.algorithm))

if not os.path.isfile(args.path):
    raise ValueError("Invalid file path: '{}'\nMust be relative or absolute path to a file.".format(args.path))

hash_func = hash_dict[args.algorithm.lower()]
if not args.quiet:
    import easygui as eg
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
                if not args.quiet:
                    box.msg = "Loading...\nProgress: {}%".format(int(self.progress))
                yield next_data
            else:
                if not args.quiet:
                    box.msg = "Complete!"
                break
    def read(self):
        if not args.quiet:            
            try:
                next_chunk = next(self.reader)
                self.data += next_chunk
                box.ui.boxRoot.after(0, self.read())
            except StopIteration:
                try:
                    box.ui.boxRoot.destroy()
                except:
                    pass
        else:
            for chunk in self.reader:
                self.data += chunk



f = FileLoader(args.path)
if not args.quiet:

    box.ui.boxRoot.after(0, f.read())
    try:
        box.run()
    except:
        pass
else:
    f.read()
result = hash_func(f.data).hexdigest()

message = """Results for {}:
{}: {}
""".format(os.path.abspath(args.path), args.algorithm.upper(), result)
print(message)
if not args.quiet:
    eg.msgbox(msg=message, title="PyFileHash")