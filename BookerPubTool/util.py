import subprocess as subp
from datetime import datetime
import requests
from pyquery import PyQuery as pq
import tempfile
import uuid
import sys
import shutil
import os
from os import path
import re
import stat

def rmtree(dir):
    files = os.listdir(dir)
    for f in files:
        f = path.join(dir, f)
        if path.isdir(f):
            rmtree(f)
        else:
            os.chmod(f, stat.S_IWUSR)
            os.unlink(f)
    os.rmdir(dir)

def d(name):
    return path.join(path.dirname(__file__), name)

def read_file(name, enco=None):
    mode = 'r' if enco else 'rb'
    with open(name, mode, encoding=enco) as f:
        return f.read()
        
def write_file(name, data, enco=None, append=False):
    mode = 'a' if append else 'w'
    if isinstance(data, bytes):
        mode += 'b'
    with open(name, mode, encoding=enco) as f:
        f.write(data)

def get_desc(md):
    rm = re.search(r'^# (.+?)$', md, re.M)
    return rm.group(1) if rm else ''
