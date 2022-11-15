## url.py module for CMT 

import time
import re
import requests
from urllib.parse import urljoin, urlparse

import globals as cmt
from checkitem import CheckItem

requests.packages.urllib3.disable_warnings()


def obfuscate_param(url):
    # http://example.com/info?a=5&b=6 >> http://example.com/info
    return urljoin(url, urlparse(url).path)  

def obfuscate_full(url):
    return "<removed>"



def check(c):

    '''Get a URL and check response code and pattern in the response body.'''

    # OUTPUT:
    # cmt_url
    # cmt_url_name
    # cmt_url_msec

    name         = c.check
    url          = c.conf['url']
    my_redirects = c.conf.get("allow_redirects", False) is True
    my_sslverify = c.conf.get("ssl_verify", False) is True
    my_host      = c.conf.get("host","")
    my_timeout   = c.conf.get("timeout",4)

    my_username = c.conf.get('username','')
    my_password = c.conf.get('password','')

    my_http_code = c.conf.get('http_code',200)

    pattern      = c.conf.get('pattern',"")
    pattern_reject  = c.conf.get('pattern_reject',"")

    obfuscate_url = c.conf.get("obfuscate_url", "param")

    # default : use env proxies
    # if "http_proxy:noenv" remove env proxies
    # else use specified proxies
    proxies = {} 
    my_http_proxy = c.conf.get('http_proxy',"")
    my_https_proxy = c.conf.get('https_proxy',my_http_proxy) 
    if my_http_proxy != "":
        proxies["http"] = my_http_proxy
    if my_https_proxy != "":
        proxies["https"] = my_https_proxy
    session = requests.Session()
    if my_http_proxy =="noenv":
        session.trust_env = False
        proxies = {}
    ##print("\n---\n",proxies)


    ci = CheckItem('url_name',name, datapoint=False)
    c.add_item(ci)

    if obfuscate_url =="param":
        url2 = obfuscate_param(url) 
    elif obfuscate_url == "full":
        url2 = obfuscate_full(url)
    else:        
        url2 = url
    ci = CheckItem('url',url2, datapoint=False)
    c.add_item(ci)


    start_time = time.time()

    headers = {}
    if my_host != "":
        headers['Host'] = my_host

    
    try:
        if len(my_username)>0:
            resp = requests.get(url, 
                headers = headers, 
                timeout=my_timeout, 
                verify=my_sslverify, 
                proxies=proxies,
                auth=(my_username, my_password),
                allow_redirects = my_redirects)
        else:
            resp = requests.get(url, 
                headers = headers, 
                timeout=my_timeout, 
                verify=my_sslverify, 
                proxies=proxies,
                allow_redirects = my_redirects)

    except Exception:
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("url {} - {} [Host: {}] - timeout/no response to query".format(name,url, my_host))
        return c

    elapsed_time = int ( 1000 * (time.time() - start_time) )
    ci = CheckItem('url_msec',elapsed_time,unit='ms')
    c.add_item(ci)

    # check http_code
    ci = CheckItem('url_httpcode',resp.status_code)
    c.add_item(ci)
    if resp.status_code != my_http_code:
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("url {} - {} [Host: {}]- bad http code response ({} received, expected {})".format(
                name,url, my_host, resp.status_code, my_http_code))
        return c


    # check for pattern, in page content AND in header
    fulltext = ""
    for k,v in resp.headers.items():
        line = "{}: {}\n".format(k,v)
        fulltext += line

    fulltext += resp.text
    #print(fulltext)

    mysearch = re.search(pattern,fulltext)
    if not mysearch:
        ci = CheckItem('url_pattern','nok')
        c.add_item(ci)
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("url {} : expected pattern not found in {} (Host: {})".format(name, url, my_host))
        return c
    else:
        ci = CheckItem('url_pattern','ok')
        c.add_item(ci)

    # check pattern_reject
    mysearch = re.search(pattern_reject,fulltext)
    if len(pattern_reject) > 0 and mysearch:
        ci = CheckItem('url_reject','nok')
        c.add_item(ci)
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("url {} : forbidden pattern found in {} (Host: {})".format(name, url, my_host))
        return c


    c.add_message("url {} - {} [Host: {}] - http={} - {} ms ; pattern OK".format(name, url, my_host, resp.status_code, elapsed_time))
    return c
