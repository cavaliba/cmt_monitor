#import psutil

import time
import re
import requests

#import globals as cmt
from checkitem import CheckItem

requests.packages.urllib3.disable_warnings()


def check(c):

    '''Get a URL and check response code and pattern in the response body.'''

    # OUTPUT:
    # cmt_url
    # cmt_url_name
    # cmt_url_msec

    name         = c.check
    url          = c.conf['url']
    pattern      = c.conf.get('pattern',"")
    my_redirects = c.conf.get("allow_redirects", False) is True
    my_sslverify = c.conf.get("ssl_verify", False) is True
    my_host      = c.conf.get("host","")
    my_timeout   = c.conf.get("timeout",4)

    # default : use env proxies
    # if "http_proxy:noenv" remove env proxies
    # else use specified proxies
    proxies = {} 
    my_http_proxy = c.conf.get('http_proxy',"")
    my_https_proxy = c.conf.get('https_proxy',my_http_proxy) 
    if my_http_proxy != "":
        proxies["http"] = my_http_proxy
    if my_http_proxy != "":
        proxies["https"] = my_https_proxy
    session = requests.Session()
    if my_http_proxy =="noenv":
        session.trust_env = False
        proxies = {}
    ##print("\n---\n",proxies)


    ci = CheckItem('url_name',name,'')
    c.add_item(ci)

    ci = CheckItem('url',url,'')
    c.add_item(ci)


    start_time = time.time()

    headers = {}
    if my_host != "":
        headers['Host'] = my_host

    
    try:
        resp = requests.get(url, 
                            headers = headers, 
                            timeout=my_timeout, 
                            verify=my_sslverify, 
                            proxies=proxies,
                            allow_redirects = my_redirects)

    except Exception:
        c.alert += 1
        c.add_message("url {} - {} [Host: {}] - timeout/no response to query".format(name,url, my_host))
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
