#!/usr/bin/env python3
'''
linkcheck - scours old posts for bad domains (et al)

Copyright Ⓒ Oli Warner, 2018

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

Depends on Python 3.6 with requests and tqdm libraries.

    sudo apt install python3-{requests,tqdm}
    python3 linkcheck.py /path/to/dump/dir
'''

import requests
from multiprocessing import Pool
import sys
import tqdm
from pathlib import Path
from functools import partial


def process_file(filepath, pool, post_id_chunk):
    with filepath.open() as source_file:
        # count lines first
        lines = sum(1 for line in source_file) 
        source_file.seek(0)

        for _ in tqdm.tqdm(pool.imap_unordered(partial(process_line, post_id_chunk=post_id_chunk), source_file), total=lines, desc=filepath.name):
            pass


def process_line(line, post_id_chunk):
    line = line.lower()

    if 'http' not in line:
        return

    for bad_domain in bad_domains:
        if bad_domain not in line:
            continue

        # get the post ID - this is the int in the post_id_chunk-th chunk
        raw_post_id = line.split(maxsplit=post_id_chunk+1)[post_id_chunk]
        post_id = ''.join(filter(lambda c: c.isdigit(), raw_post_id))
        print(f'https://askubuntu.com/q/{post_id}/\t{bad_domain}')


if __name__ == "__main__":
    try:
        dumpdir = Path(sys.argv[1])
        if not (dumpdir.exists() and dumpdir.is_dir() and (dumpdir / 'Posts.xml').exists()):
            raise IndexError()
    except IndexError:
        sys.stderr.write('Missing path to dump dir!\n')
        sys.exit(1)

    # Read in the blacklisted_websites
    # This is modified from the Smoke Detector
    with (Path(__file__).parent / 'smokey/blacklisted_websites.txt').open() as f:
        bad_domains = f.read().lower().splitlines()

    pool = Pool()
    process_file(dumpdir / 'Posts.xml', pool, post_id_chunk=1)
    process_file(dumpdir / 'Comments.xml', pool, post_id_chunk=2)
