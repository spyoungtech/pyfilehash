import argparse
from hashlib import md5, sha1, sha224, sha256, sha384, sha512
import os
import time
import sys

class FileLoader(object):
    def __init__(self, fp, algorithm):
        self.fp = fp
        self.file_size = os.stat(self.fp).st_size
        self.chunk_size = int(self.file_size / 500) - 1 
        self.file = open(self.fp, 'rb')
        self.progress = 0
        if algorithm == "*":
            self.hashes = {algo: hash_dict[algo]() for algo in hash_dict if algo != "*"}
        else:
            self.hashes = {algorithm: hash_dict[algorithm]()}
        self.progress_incr = 100 / (self.file_size / self.chunk_size)
        self.reader = self.chunk_reader()
        self.complete= False

    def update(self, next_data):
        for _, h in self.hashes.items():
            h.update(next_data)

    def chunk_reader(self):
        while True:
            next_data = self.file.read(self.chunk_size)
            if next_data:
                self.progress += self.progress_incr
                self.update(next_data)
                if not args.quiet:
                    box.msg = "Loading...\nProgress: {}%".format(int(self.progress))
                yield
            else:
                if not args.quiet:
                    box.msg = "Complete!"
                break
    def read(self):
        if not args.quiet:            
            try:
                next_chunk = next(self.reader)
                box.ui.boxRoot.after(0, self.read)
            except StopIteration:
                self.complete = True
                try: 
                    box.ui.boxRoot.destroy()
                except:
                    pass
        else:
            for chunk in self.reader:
                pass


hash_dict = {"md5": md5,
             "sha1": sha1,
             "sha224": sha224,
             "sha256": sha256,
             "sha384": sha384,
             "sha512": sha512,
             "*": "*"}

parser = argparse.ArgumentParser()
parser.add_argument("algorithm", help="The algorithm to use, I.E MD5, SHA1, SHA256, etc.",)
parser.add_argument("path", help="The path of the file. Can be relative or absolute.")
parser.add_argument("-q", "--quiet", action="store_true", help="Quiet flag. Supresses GUI")
args = parser.parse_args()



if args.algorithm.lower() not in hash_dict:
    raise ValueError("Invalid algorithm '{}'".format(args.algorithm))

if not os.path.isfile(args.path):
    raise ValueError("Invalid file path: '{}'\nMust be relative or absolute path to a file.".format(args.path))

#hash_func = hash_dict[args.algorithm.lower()]

if not args.quiet:
    import easygui as eg
    box = eg.buttonbox(msg="Loading...\nProgress: 0%", title="PyFileHash", choices=["Cancel"], cancel_choice="Cancel", run=False)
    icon_path = __file__.replace("pyfilehash.py", "pfh.ico")
    box.ui.boxRoot.iconbitmap(icon_path)

start = time.time()

f = FileLoader(args.path, args.algorithm.lower())
if not args.quiet:
    box.ui.boxRoot.after(0, f.read)
    try:
        box.run()
    except Exception as e:
        pass

if not f.complete:
    sys.exit(1)

else:
    f.read()


hashes = {algo: h.hexdigest() for algo, h in f.hashes.items()}
end = time.time()
t = end - start
results = '\n\n'.join("{}: {}".format(algo.upper(), h) for algo, h in sorted(hashes.items()))

message = "Results for {}:\n\n{}\nCompleted in {} seconds".format(os.path.abspath(args.path), results,t )
print(message)
if not args.quiet:
    mbox = eg.buttonbox(msg=message, title="PyFileHash", choices=["OK"], cancel_choice="OK", run=False)
    mbox.ui.boxRoot.iconbitmap(icon_path)
    mbox.run()