import re
import os
from os import path
import shutil
import sys
import subprocess as subp
import zipfile
from io import BytesIO
from .util import *

README_TMP = '''
# {title}

## 下载

### Docker

```
docker pull apachecn0/{docker_hub_name}
docker run -tid -p <port>:80 apachecn0/{docker_hub_name}
# 访问 http://localhost:{port} 查看文档
```

### PYPI

```
pip install {pip_name}
{pip_name} <port>
# 访问 http://localhost:{port} 查看文档
```

### NPM

```
npm install -g {npm_name}
{npm_name} <port>
# 访问 http://localhost:{port} 查看文档
```
'''

INDEX_HTML = '''
<html>
<head></head>
<body style="margin: 0;">
    <iframe src='file.pdf' style='width: 100%; height: 100%; border: 0;'></iframe>
</body>
</html>
'''

def ebook2site(args):
    name = args.name
    fname = args.file
    dir = args.dir
    
    if not fname.endswith('.pdf') and \
       not fname.endswith('.epub'):
        print('请提供 PDF 或 EPUB')
        return 
    
    proj_dir = path.join(dir, name)
    os.mkdir(proj_dir)
    
    if fname.endswith('.pdf'):
        shutil.copy(fname, path.join(proj_dir, 'file.pdf'))
        open(path.join(proj_dir, 'index.html'), 'w', encoding='utf8').write(INDEX_HTML)
    else:
        shutil.copy(fname, path.join(proj_dir, 'file.epub'))
        zip = zipfile.ZipFile(BytesIO(open('epubjs-reader.zip', 'rb').read()))
        for f in zip.namelist(): zip.extract(f, proj_dir)
        zip.close()
    title = path.basename(fname).replace('.pdf', '').replace('.epub', '')
    npm_name = npm_filter_name(name)
    README_MD = README_TMP \
        .replace('{title}', title) \
        .replace('{docker_hub_name}', name) \
        .replace('{pip_name}', name) \
        .replace('{npm_name}', npm_name)
    open(path.join(proj_dir, 'README.md'), 'w', encoding='utf8').write(README_MD)
