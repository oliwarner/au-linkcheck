# Ask Ubuntu linkcheck.py

The aim of this little script is simple: check to make sure that old posts don't have links to crappy old domains and URLs in them. Many of these are detected after the fact [citation needed] and while Smoke Detector (et al) do a fine job with new posts and edits, they're no good helping us take out the trash.

**Disclaimer**: As always, focus should be on dealing with new questions, not letting them rot while we clear up the old rubbish, but this seemed like a genuine hole in the way we handle things. A fun little programming project, regardless.

This script relies on the speed of pypy3 to actually get anything done. It creates a HUGE regex that is just too slow on the standard Python3 interpreter. 100it/s vs 1.5it/s. I'm sure some work could be done here to speed it up even more (PRs accepted!) but this is as far as I can walk it for now.

On Ubuntu 18.04, the following will install `pypy3` and the depencencies that `linkcheck.py` requires:

    sudo snap install pypy3 --classic
    pypy3 -m ensurepip --user
    pypy3 -m pip --user install requests tqdm

Then download the data dump from https://archive.org/download/stackexchange (600MB for Ask Ubuntu) extract it, copy `linkcheck.py` into the directory with those files, and run it:

    /snap/bin/pypy3 linkcheck.py /path/to/dump/dir

It will then buzz through the Posts and then the comments looking for bad links.

You can also enable a bad keyword search but this is a lot slower.
