import re
import os
from os import path
import shutil
import sys
import subprocess as subp
import zipfile
import jieba
import xpinyin
from io import BytesIO
from .util import *

def gen_proj_name(name):
    name = re.sub(r'\.\w+$', '', name.lower())
    seg = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z0-9]+', name)
    nseg = []
    p = xpinyin.Pinyin()
    for s in seg:
        if re.search(r'[a-zA-Z0-9]', s):
            nseg.append(s)
        else:
            subseg = jieba.cut(s)
            for ss in subseg:
                nseg.append(p.get_pinyin(ss).replace('-', ''))
    res = '-'.join(nseg)
    return res

def ebook2site(args):
    name = args.name
    fname = args.file
    dir = args.dir
        
    if not fname.endswith('.pdf') and \
       not fname.endswith('.epub'):
        print('请提供 PDF 或 EPUB')
        return 
    
    if not name: name = gen_proj_name(path.basename(fname))
    proj_dir = path.join(dir, name)
    os.mkdir(proj_dir)
    
    if fname.endswith('.pdf'):
        shutil.copy(fname, path.join(proj_dir, 'file.pdf'))
        shutil.copy(
            d('asset/pdf.html'), 
            path.join(proj_dir, 'index.html'),
        )
    else:
        shutil.copy(fname, path.join(proj_dir, 'file.epub'))
        zip = zipfile.ZipFile(BytesIO(open(d('asset/epubjs-reader.zip'), 'rb').read()))
        for f in zip.namelist(): zip.extract(f, proj_dir)
        zip.close()
    title = path.basename(fname).replace('.pdf', '').replace('.epub', '')
    npm_name = npm_filter_name(name)
    README_TMP = read_file(d('asset/readme.tmpl'), 'utf-8')
    README_MD = README_TMP \
        .replace('{title}', title) \
        .replace('{docker_hub_name}', name) \
        .replace('{pip_name}', name) \
        .replace('{npm_name}', npm_name)
    open(path.join(proj_dir, 'README.md'), 'w', encoding='utf8').write(README_MD)
