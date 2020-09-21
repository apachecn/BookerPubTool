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
from . import *
    
def publish(dir):
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
    mod_name = get_module_name(name)
    now = datetime.now()
    ver = f'{now.year}.{now.month}.{now.day}.' + \
          str(get_new_version(name))
    readme = read_file(path.join(dir, 'README.md'), 'utf-8')
    desc = get_desc(readme)
    print(f'name: {name}, mod: {mod_name}, ver: {ver}, desc: {desc}')
    # 创建临时目录
    pkg_dir = path.join(tempfile.gettempdir(), uuid.uuid4().hex)
    os.mkdir(pkg_dir)
    # 填充文档
    shutil.copytree(dir, path.join(pkg_dir, mod_name))
    shutil.copy(
        path.join(pkg_dir, mod_name, 'README.md'),
        path.join(pkg_dir, 'README.md')
    )
    # 主程序
    shutil.copy(
        d('asset/server.py'),
        path.join(pkg_dir, mod_name, '__main__.py')
    )
    # 配置
    setup_py = read_file(d('asset/setup.tmpl'), 'utf-8')
    setup_py = setup_py.replace('{mod}', mod_name) \
                       .replace('{name}', name) \
                       .replace('{desc}', desc)
    write_file(path.join(pkg_dir, 'setup.py'), setup_py, 'utf-8')
    init_py = read_file(d('asset/__init__.tmpl'), 'utf-8')
    init_py = init_py.replace('{name}', name) \
                     .replace('{ver}', ver)
    write_file(
        path.join(pkg_dir, mod_name, '__init__.py'),
        init_py, 'utf-8'
    )
    # 发布
    un = subp.Popen(
        ['pip', 'config', 'get', 'pypi.username'],
        stdout=subp.PIPE,
        stderr=subp.PIPE,
        shell=True
    ).communicate()[0]
    pw = subp.Popen(
        ['pip', 'config', 'get', 'pypi.password'],
        stdout=subp.PIPE,
        stderr=subp.PIPE,
        shell=True
    ).communicate()[0]
    un, pw = un.decode().strip(), pw.decode().strip()
    os.chdir(pkg_dir)
    subp.Popen(
        ['python', 'setup.py', 'sdist', 'bdist_wheel'],
        shell=True
    ).communicate()
    subp.Popen(
        ['twine', 'upload', 'dist/*', '-u', un, '-p', pw],
        shell=True
    ).communicate()
    # 删除临时目录
    os.chdir('..')
    rmtree(pkg_dir)
    
def main():
    publish(sys.argv[1])
    
if __name__ == '__main__': main()