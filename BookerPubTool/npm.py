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
import json
from .util import *

def config_npm(args):
    subp.Popen(
        ['npm', 'config', 'set', '//registry.npmjs.org/:_authToken', args.token],
        shell=True,
        stdout=subp.PIPE,
        stderr=subp.PIPE
    ).communicate()
    
def publish_npm(args):
    dir = args.dir
    if dir.endswith('/') or \
       dir.endswith('\\'):
        dir = dir[:-1]
    # 检查目录
    if not path.isdir(dir):
        print('请提供目录')
        return
    files = os.listdir(dir)
    if not 'index.html' in files or \
       not 'README.md' in files:
        print('请提供文档')
        return
    # 读取元信息
    name = path.basename(dir)
    pkg_name = npm_filter_name(name)
    now = datetime.now()
    ver = f'{now.year}.{now.month}.{now.day}.' + \
          str(get_pypi_new_version(name))
    readme = read_file(path.join(dir, 'README.md'), 'utf-8')
    desc = get_desc(readme)
    print(f'name: {name}, mod: {mod_name}, ver: {ver}, desc: {desc}')
    # 创建临时目录
    pkg_dir = path.join(tempfile.gettempdir(), uuid.uuid4().hex)
    os.mkdir(pkg_dir)
    # 填充文档
    shutil.copytree(dir, path.join(pkg_dir, 'doc'))
    shutil.copy(
        path.join(pkg_dir, 'doc/README.md'),
        path.join(pkg_dir, 'README.md')
    )
    # 主程序
    shutil.copy(
        d('asset/server.js'),
        path.join(pkg_dir, 'index.js')
    )
    # 配置
    pkg_json = json.loads(read_file(d('asset/package.tmpl'), 'utf-8'))
    pkg_json['name'] = pkg_name
    pkg_json['version'] = ver
    pkg_json['description'] = desc
    pkg_json['repository']['url'] = \
        f'git+https://github.com/apachecn/{name}.git'
    pkg_json['bin'] = {}
    pkg_json['bin'][pkg_name] = "index.js"
    pkg_json['bin'][name] = "index.js"
    write_file(
        path.join(pkg_dir, 'package.json'),
        json.dumps(pkg_json), 'utf-8'
    )
    # 发布
    os.chdir(pkg_dir)
    subp.Popen(
        ['npm', 'publish'],
        shell=True
    ).communicate()
    # 删除临时目录
    os.chdir('..')
    rmtree(pkg_dir)
