VERSION="0.1"

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from optparse import OptionParser

import os
import errno
import requests as req 


option_parser = OptionParser(usage="Usage: %prog [options] [url1] [url2] ...", version=f"%%prog v{VERSION}")
option_parser.add_option('-l', '--link', action='store', dest='url_list_file',
                         help='Link to Anime', metavar='LINK')

option_parser.add_option('-o', '--output', action='store', dest='output_dir', default='./',
                         help='DIRECTORY to save downloaded files to', metavar='/path/to/destination/')

option_parser.add_option('-b', '--begin', action='store', dest='begin_ep', default='1',
                         help='Episode to start download. 1 is default', metavar='BEGIN')

option_parser.add_option('-e', '--end', action='store', dest='end_ep', default='0',
                         help='Episode to end download. len is default', metavar='END')

(options, args) = option_parser.parse_args()

anime_link = options.url_list_file
output_dir = options.output_dir
begin_ep = int(options.begin_ep)
end_ep = int(options.end_ep)

if output_dir[-1] != '/': output_dir += '/'

if not os.path.exists(os.path.dirname(output_dir)):
    try:
        os.makedirs(os.path.dirname(output_dir))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

### get links on anbient
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

if anime_link is None or anime_link == "":
    print("Use -l or --link to add link to anime")
    exit(0)

driver.get(anime_link)
html = driver.page_source

soup = BeautifulSoup(html, 'html5lib')
#print(soup)

block = soup.find('div', class_ = 'servidor zippyshare active')

if block is None: 
    block = soup.find('div', class_ = 'servidor zippyshare')

    if block is None:
        print("Anime dont have support to zippyshare")
        exit(0)
        
block_li = block.find_all('li')

links = []

for li in block_li:
    lia = li.find('a', href=True)
    links.append(lia['href'])

# Download
if end_ep == 0: end_ep = len(links)

if end_ep > len(links): end_ep = len(links)

for i in range(begin_ep-1, end_ep):
    driver.get(links[i])
    html = driver.page_source

    soup = BeautifulSoup(html)
    
    endpoint = soup.find(id='dlbutton', href=True)

    zip_url = links[i].find("/", 10)


    dl_url = links[i][:zip_url] + endpoint['href']

    file_name = dl_url.split('/')[-1]  

    print( "Downloading file:%s"%file_name)  
        
    # create response object  
    r = req.get(dl_url, stream = True)  
        
    # download started  
    with open(output_dir + file_name, 'wb') as f:  
        for chunk in r.iter_content(chunk_size = 1024*1024):  
            if chunk:  
                f.write(chunk)  
        
    print( "%s downloaded!\n"%file_name ) 
