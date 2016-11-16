# PyFileHash

PyFileHash is a utility for getting file checksums.

Supports md5, sha1, sha224, sha256, sha384, and sha512

#Usage
```
usage: pyfilehash.py [-h] [-q] algorithm path

positional arguments:
  algorithm    The algorithm to use, I.E MD5, SHA1, SHA256, etc.
  path         The path of the file. Can be relative or absolute.

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  Quiet flag. Supresses GUI
```