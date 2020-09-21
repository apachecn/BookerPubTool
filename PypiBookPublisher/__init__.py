#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

"""pypi-book-publisher
https://github.com/apachecn/pypi-book-publisher"""

__author__ = "ApacheCN"
__email__ = "apachecn@163.com"
__license__ = "SATA"
__version__ = "2020.9.21.0"


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

def config(un, pw):
    subp.Popen(
        ['pip', 'config', 'set', 'pypi.username', un],
        shell=True,
        stdout=subp.PIPE,
        stderr=subp.PIPE
    ).communicate()
    subp.Popen(
        ['pip', 'config', 'set', 'pypi.password', pw],
        shell=True,
        stdout=subp.PIPE,
        stderr=subp.PIPE
    ).communicate()
    
def get_new_version(name, curr=None):
    now = datetime.now()
    curr = curr or \
        f'{now.year}.{now.month}.{now.day}'
    r = requests.get(f'https://pypi.org/project/{name}/')
    if r.status_code == 404:
        return 0
    root = pq(r.text)
    ver = root('h1.package-header__name')[0] \
            .text.strip() \
            .split(' ')[1]
    if not ver.startswith(curr + '.'):
        return 0
    else:
        return int(ver.split('.')[-1]) + 1
    
def get_module_name(name):
    name = name.replace('_', '-')
    name = re.sub(r'[^\w\-]', '-', name)
    names = filter(None, name.split('-'))
    names = [n.capitalize() for n in names]
    return ''.join(names)