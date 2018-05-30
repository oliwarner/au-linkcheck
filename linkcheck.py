#!/snap/bin/pypy3
'''
linkcheck - scours old posts for bad domains (et al)

Copyright Ⓒ Oli Warner, 2018

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.


This NEEDS pypy to run at any sort of decent speed.

    sudo snap install pypy3 --classic
    pypy3 -m ensurepip --user
    pypy3 -m pip --user install requests tqdm

Download the dumps from https://archive.org/download/stackexchange  
Extract it somewhere, then run:

    /snap/bin/pypy3 linkcheck.py /path/to/dump/dir
'''

import re
import requests
from multiprocessing import Pool
import sys
import tqdm
from pathlib import Path
from functools import partial


BAD_FILES = [
    'https://raw.githubusercontent.com/Charcoal-SE/SmokeDetector/master/blacklisted_websites.txt',
    # 'https://raw.githubusercontent.com/Charcoal-SE/SmokeDetector/master/bad_keywords.txt',  # disabled for speed
]


def process_file(filepath, pool, post_id_chunk):
    with filepath.open() as source_file:
        # count lines first
        lines = sum(1 for line in source_file) 
        source_file.seek(0)

        for _ in tqdm.tqdm(pool.imap_unordered(partial(process_line, post_id_chunk=post_id_chunk), source_file), total=lines, desc=filepath.name):
            pass


def process_line(line, post_id_chunk):
    if regex.search(line) is not None:
        # get the post ID - this is the int in the post_id_chunk-th chunk
        raw_post_id = line.split(maxsplit=post_id_chunk+1)[post_id_chunk]
        post_id = ''.join(filter(lambda c: c.isdigit(), raw_post_id))
        print(f'https://askubuntu.com/q/{post_id}/')


if __name__ == "__main__":
    try:
        dumpdir = Path(sys.argv[1])
        if not (dumpdir.exists() and dumpdir.is_dir() and (dumpdir / 'Posts.xml').exists()):
            raise IndexError()
    except IndexError:
        sys.stderr.write('Missing path to dump dir!\n')
        sys.exit(1)

    # We start by turning the Smoke Detector lists into one big
    # regex from hell: (keyword)|(keyword2)|...
    # There's certainly a better way to do this! There has to be. PR please!
    regexes = '\n'.join(requests.get(url).text for url in BAD_FILES)
    regex = re.compile('|'.join(f'({reg})' for reg in regexes.split('\n') if reg), re.I)

    pool = Pool()
    process_file(dumpdir / 'Posts.xml', pool, post_id_chunk=1)
    # process_file(dumpdir / 'Comments-test.xml', pool, post_id_chunk=2)
