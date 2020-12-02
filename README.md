# AnbientDown
 
Anbient download script, written in Python.

Downloads Episodes using the link of anime on anbient. You can provide the URLs on the command line.

# Requirements
* Python 3.6 (or above)
  * bs4
  * selenium
  * webdriver_manager
  * optparse
  * requests

Install dependencies automatically with pip:

    pip3 install -r requirements.txt

# Usage
    $ python3 AnbientDown.py -h
    Usage: zipPy.py [options] [url1] [url2] ...
    
    Options:
        --version             show program's version number and exit
        -h, --help            show this help message and exit
        -l LINK, --link=LINK  Link to Anime
        -o /path/to/destination/, --output=/path/to/destination/
                                DIRECTORY to save downloaded files to
        -b BEGIN, --begin=BEGIN
                                Episode to start download. 1 is default
        -e END, --end=END     Episode to end download. len is default

# Changelog

## v0.1
* Initial release