#import psutil

import time
import re
import requests
requests.packages.urllib3.disable_warnings()


import cmt_globals as cmt
from cmt_shared import Check, CheckItem

def check_url(c):

    '''Get a URL and check response code and pattern in the response body.'''

    # OUTPUT:
    # cmt_url
    # cmt_url_name
    # cmt_url_msec

    name         = c.check
    url          = c.conf['url']
    pattern      = c.conf.get('pattern',"")
    my_redirects = c.conf.get("allow_redirects",False) == True
    my_sslverify = c.conf.get("ssl_verify",False) == True
    my_host      = c.conf.get("host","")

    ci = CheckItem('url_name',name,'')
    c.add_item(ci)

    ci = CheckItem('url',url,'')
    c.add_item(ci)


    start_time = time.time()

    headers = {}
    if my_host != "":
        headers['Host'] = my_host

    try:
        resp = requests.get(url, headers = headers, timeout=5, verify=my_sslverify, allow_redirects = my_redirects)
    except:
        c.alert += 1
        c.add_message("url {} - {} [Host: {}] - no response to query".format(name,url, my_host))
        return c

    elapsed_time = int ( 1000 * (time.time() - start_time) )
    ci = CheckItem('url_msec',elapsed_time,unit='ms')
    c.add_item(ci) 

    if resp.status_code != 200:
        c.alert += 1
        c.add_message("url {} - {} [Host: {}]- bad http code response ({})".format(name,url, my_host, resp.status_code))
        return c

    # check pattern
    mysearch = re.search(pattern,resp.text)
    if not mysearch:
        c.alert += 1
        c.add_message("url expected pattern not found for {} ({} [Host: {}])".format(name, url, my_sslverify))
        return c

    c.add_message("url {} - {} [Host: {}] - http={} - {} ms ; pattern OK".format(name, url, my_host, resp.status_code, elapsed_time))
    return c

