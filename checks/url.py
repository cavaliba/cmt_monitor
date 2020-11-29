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

    name         = c.name
    url          = c.conf['url']
    pattern      = c.conf.get('pattern',"")
    my_redirects = c.conf.get("allow_redirects",False) == True
    my_sslverify = c.conf.get("ssl_verify",False) == True

    ci = CheckItem('url_name',name,'')
    c.add_item(ci)

    ci = CheckItem('url',url,'')
    c.add_item(ci)


    start_time = time.time()

    try:
        resp = requests.get(url, timeout=5, verify=my_sslverify, allow_redirects = my_redirects)
    except:
        c.alert += 1
        c.add_message("{} - {} - no response to query".format(name,url))
        return c

    elapsed_time = int ( 1000 * (time.time() - start_time) )
    ci = CheckItem('url_msec',elapsed_time,unit='ms')
    c.add_item(ci) 

    if resp.status_code != 200:
        c.alert += 1
        c.add_message("{} - {} - bad http code response ({})".format(name,url, resp.status_code))
        return c

    # check pattern
    mysearch = re.search(pattern,resp.text)
    if not mysearch:
        c.alert += 1
        c.add_message("expected pattern not found for {} ({})".format(name, url))
        return c

    c.add_message("{} - {} - http={} - {} ms ; pattern OK".format(name, url, resp.status_code, elapsed_time))
    return c

