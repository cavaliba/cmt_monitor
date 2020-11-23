---
title: check_urls
---

# Urls

**URLS** checks if one or more *Url* can 

- be contacted before a timeout, 
-  provides an http response code of 200 (OK)
-  contains a specific pattern / string in the body of the response.

It can verify TLS/SSL certificates.
It can follow redirets.
It reports URL response time.

This check can be used from a remote server to monitor various URL and Webservices. It can also be configured locally on a single Webserver to monitor a local single instance. If the provided URL is an application status (e.g. php-fpm /status with pattern "pong"), you can have a basic (or not so basic) application monitor.

## Enable the check

Enable de `urls` check in the configuration :

    # conf.yml
	checks:
  	  - urls

## Additional parameters

This check requires additional parameters to define each URL to be checked :

	# conf.py
	urls:
	  - url: https://www.cavaliba.com/
	    name: www.cavaliba.com
	    pattern: "Cavaliba"
	    allow_redirects: yes
	    ssl_verify: yes
	  - url: http://demo.cavaliba.com/
	    name: demo.cavaliba.com
	    pattern: "SIRENE"

pattern: 
	
    the string to be searched in the response body

allow_redirects:
	
    CMT will follow redirects

ssl_verify:
	
    CMT will check for a valid TLS certificate (CA, validity, host)


## Alerts

This check sends an alert and adds alert fields if an URL isn't responding properly.

output:

	cmt_alert: yes
	cmt_alert_message: string

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
	--------------------------------------------------
	CMT - Version 0.9 - (c) Cavaliba.com - 2020/10/20
	2020/10/25 - 20:40:36 : Starting ...
	--------------------------------------------------
	cmt_group :  cmtdev
	cmt_node  :  vmpio

	Check url 
	cmt_url_name           demo.cavaliba.com             
	cmt_url                http://demo.cavaliba.com/     
	cmt_url_msec           227 ms                        
	cmt_url_status         OK                   

	No alerts. 





