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

def ebook2site(fname, odir):
    if path.isdir(odir):
        shutil.rmtree(odir)
    os.makedirs(odir)
    m = re.search(r'\.(\w+)$', fname)
    ext = m.group(1) if m else ''
    if ext == 'pdf':
        shutil.copy(fname, path.join(odir, 'file.pdf'))
        shutil.copy(
            d('asset/pdf.html'), 
            path.join(odir, 'index.html'),
        )
    elif ext in ['epub', 'mobi', 'azw3']:
        tmp_fname = path.join(odir, 'file.epub')
        if ext in ['mobi', 'azw3']:
            r = subp.Popen(
                ['ebook-convert', fname, tmp_fname], 
                shell=True,
                stdout = subp.PIPE,
                stderr = subp.PIPE,
            ).communicate()
            print((r[0] or r[1] or b'').decode('utf8', 'ignore'))
        else:
            shutil.copy(fname, tmp_fname)
        zip = zipfile.ZipFile(BytesIO(open(d('asset/epubjs-reader.zip'), 'rb').read()))
        for f in zip.namelist(): zip.extract(f, odir)
        zip.close()
    else:
        raise ValueError('文件必须是 PDF、EPUB、MOBI 或 AZW3')
    title = path.basename(fname).replace('.pdf', '').replace('.epub', '')
    name = path.basename(path.abspath(odir))
    npm_name = npm_filter_name(name)
    README_TMP = read_file(d('asset/readme.tmpl'), 'utf-8')
    README_MD = README_TMP \
        .replace('{title}', title) \
        .replace('{docker_hub_name}', name) \
        .replace('{pip_name}', name) \
        .replace('{npm_name}', npm_name)
    open(path.join(odir, 'README.md'), 'w', encoding='utf8').write(README_MD)

def ebook2site_handle(args):
    name = args.name
    fname = args.file
    dir = args.dir
        
    if not fname.endswith('.pdf') and \
       not fname.endswith('.epub'):
        print('请提供 PDF 或 EPUB')
        return 
    
    if not name: name = gen_proj_name(path.basename(fname))
    proj_dir = path.join(dir, name)
    ebook2site(fname, proj_dir)
    
