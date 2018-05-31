# Ask Ubuntu linkcheck.py

The aim of this little script is simple: check to make sure that old posts don't have links to crappy old domains and URLs in them. Many of these are detected after the fact [citation needed] and while Smoke Detector (et al) do a fine job with new posts and edits, they're no good helping us take out the trash.

> **Disclaimer**: As always, focus should be on dealing with new questions, not letting them rot while we clear up the old rubbish, but this seemed like a genuine hole in the way we handle things. A fun little programming project, regardless.

This script requires Python 3.6 (because I'm lazy and like new things) and the requests and tqdm libraries. On Ubuntu 18.04, getting up and running is as simple as:

	sudo apt install git python3-{requests,tqdm}
	git clone https://github.com/oliwarner/au-linkcheck.git
	/usr/bin/python3 au-linkcheck/linkcheck.py /path/to/dump/directory

Obviously you'll need to download a dump to run this again from https://archive.org/download/stackexchange  
These aren't small —600MB for Ask Ubuntu— but extract it and point linkcheck at it.

On a fast desktop (7700K@5GHz + 3GB/s SSD) you can chow through Ask Ubuntu's 1.5 million posts and comments in under a minute.
