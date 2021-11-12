---
title: check_urls
---

# Url

**URL** checks if one or more *Url* can 

- be contacted before a timeout, 
- provides an http response code of 200 (OK)
- contains a specific pattern / string in the body of the response.

It can verify TLS/SSL certificates.
It can follow redirets.
It reports URL response time.
It can pass a Host header to query specfic virtual-host.

This check can be used from a remote server to monitor various URL and Webservices. It can also be configured locally on a single Webserver to monitor a local single instance. If the provided URL is an application status (e.g. php-fpm /status with pattern "pong"), you can have a basic (or not so basic) application monitor.

## Configure

	# conf.yml
	url:
	    www.cavaliba.com:
			url               : https://www.cavaliba.com/
			[allow_redirects] : yes ; default = no
			[ssl_verify]      : yes ; default = no
			[host]            : optionnal hostname header (Host: xxx) ; default to None
			[timeout]         : float (sec) ; default = 4 ; e.g. : 5.2
			[http_proxy]      : http://[login[:pass]@proxyhost:port  ; use noenv value to skip os/env			
			[https_proxy]     : https://[login[:pass]]@proxyhost:port  ; default to http_proxy
			[username]        : login to be provided to basic/digest auth by remote webserver
			[password]        : password to be provided to basic/digest auth by remote webserver
			[http_code]       : expected code ; default 200
			[pattern]         : pattern expected in response (default none) 
			[pattern_reject]  : pattern to NOT find in response (default none)

pattern: 
	
	default: non
    a string / regexp (python re.) which MUST be present in the response body
    
pattern_reject: 

	new: 2.0
	default: none	
    a string / regexp (python re.) which MUST NOT be present in the response body
    useful to check for no error message in a status page

allow_redirects:
	
    CMT will follow HTTP redirects

ssl_verify:
	
    CMT will check for a valid TLS certificate (CA, validity, host)

host: 

    add a Host: header to specify which target/virtualhost to query

timeout:

    socket timeout value (no bytes lapse) ; default : 4 secs. Float accepted

http_proxy:

	default : use os/env wide settings.
	if defined, use specified proxy for http requests. 
	http://[login[:pass]]@proxyhost:port
	use noenv value to skip os/env (direct access)

https_proxy

	default : http_proxy 
	if defined, use specified proxy for https (TLS/SSL) requests. 
	https://[login[:pass]]@proxyhost:port	

username, password

    new in 2.0
    default : no authentication sent to remote server

http_code

    new in 2.0
    default : 200
    expected http_code in response
    useful to check non-200 responses like redirects 30X, forbidden 40X, webservice specials 20X, etc.



## Alerts

This check sends an alert and adds alert fields if an URL isn't responding properly.

Alert message:

- no response to query (timeout / no response)
- bad http code response
- expected pattern not found

## Output to Metrology

This module sends one message for each URL, with the following fields:

	cmt_check: url
	+
	cmt_url:  url string
	cmt_url_name: url name
	cmt_url_status: ok/nok
	cmt_url_msec: int        [response time in millisecond if available]

## CLI usage and output

	$ ./cmt.py urls

	Check url 
	cmt_url_name           www.cavaliba.com  () 
	cmt_url                https://www.cavaliba.com/  () 
	cmt_url_msec           96 ms () 
	OK                     www.cavaliba.com - https://www.cavaliba.com/ [Host: ] - http=200 - 96 ms ; pattern OK

	Check url 
	cmt_url_name           www_non_existing  () 
	cmt_url                http://www.nonexisting/  () 
	NOK                    www_non_existing - http://www.nonexisting/ [Host: ] - no response to query

	Check url 
	cmt_url_name           demo.cavaliba.com  () 
	cmt_url                http://demo.cavaliba.com/  () 
	cmt_url_msec           187 ms () 
	OK                     demo.cavaliba.com - http://demo.cavaliba.com/ [Host: ] - http=200 - 187 ms ; pattern OK






