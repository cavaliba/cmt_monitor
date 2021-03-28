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

## Enable the module

Enable the module in the configuration (optional) :

    # conf.yml
    
	modules:
  	  url:
  	     enable: yes

## configure URL checks 

### common parameters

See [config page](config.md) for common check parameters.

### specific parameters

	# conf.yml
	url:
	    www.cavaliba.com:
			url               : https://www.cavaliba.com/
			[pattern]         : "Cavaliba" ; DEFAULT = ""
			[allow_redirects] : yes ; default = no
			[ssl_verify]      : yes ; default = no
			[host]            : optionnal hostname header (Host: xxx) ; default to None
			[timeout]         : float (sec) ; default = 4 ; e.g. : 5.2
			[http_proxy]      : http://[login[:pass]@proxyhost:port  ; use noenv value to skip os/env			
			[https_proxy]     : https://[login[:pass]]@proxyhost:port  ; default to http_proxy


pattern: 
	
    the string to be searched in the response body

allow_redirects:
	
    CMT will follow redirects

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

## Alerts

This check sends an alert and adds alert fields if an URL isn't responding properly.

Alert message:

- no response to query (timeout / no response)
- bad http code response
- expected pattern not found

## Output to ElasticSearch

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






