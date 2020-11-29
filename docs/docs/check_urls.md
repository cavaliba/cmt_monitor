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

Enable de module in the configuration :

    # conf.yml

	Module:
  	  url:
  	     enable: yes

## Additional parameters

This check requires additional parameters to define each URL to be checked :

	# conf.py
	# url
	  www.cavaliba.com:
	    module: url
	    enabled: after 2020-01-01
	    url: https://www.cavaliba.com/
	    pattern: "Cavaliba"
	    allow_redirects: yes
	    ssl_verify: yes
	    #host: toto
	  www_non_existing:
	    module: url
	    enabled: after 2020-01-01
	    url: http://www.nonexisting/
	    #pattern: ""


pattern: 
	
    the string to be searched in the response body

allow_redirects:
	
    CMT will follow redirects

ssl_verify:
	
    CMT will check for a valid TLS certificate (CA, validity, host)


## Alerts

This check sends an alert and adds alert fields if an URL isn't responding properly.

Alert message:

- no response to query (timeout / no response)
- bad http code response
- expected pattern not found

## Output to ElasticSearch

This module sends one message for each mount point, with the following fields:

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






