---
title: Pager and alerts
---


# Concepts : severity, alerts, pagers

Use wisely, syadmin sleep is precious !


## Severity

In CMT, `severity` is the result of an indivudal check and refers to the state of the target of the check. It can have one of the following values:

	1 SEVERITY_CRITICAL
	2 SEVERITY_ERROR
	3 SEVERITY_WARNING
	4 SEVERITY_NOTICE
	5 SEVERITY_NONE

Severity doesn't carry any alerting concept. It's just an immediate state observation for a specific target.

## Alerts

An `alert` is a decision to notify certain remote systems (pagers, metrology) about a new or continuing state  of abnormality. Alert can take one oif the following values:

	ALERT_NEW : alert is new, transition from SEVERITY_NONE to SEVERITY_XXX, after an alert_delay.
	ALERT_ACTIVE : alert is on-going, severity is still not NONE, without interruption
	ALERT_DOWN : severity has become NONE again
	ALERT_NONE : severity is NONE , no alert

Any severity can triger an alert.

Checks configuration should implement `severity_max` to limit or cap max severity for said checks. Not all checks results are tha important !

E.g.:

	- check for the URL of the main production application should have a severity criticial or error at least.
	- check for memory consumption could be well in the notice/warning range

## Pagers

At the end, `pagers` are remote devices to which CMT may send alerts.

Supported type:

		* team_channel
		* teams (same as team)
		* pagerduty (experimental)

All events sent to metrology also have severity/alert fields which carry information about alerting.

## global configuration

	global:
        (...)
        enable: yes
        enable_pager: yes
        alert_delay: 90
		(...)


## Check configuration

Each check must explicitly have the option `enable_pager` to permit an alert for this check. 


    a_module:

       my_check:
           enable: yes
           severity_max: error
           enable_pager: business_hours
           alert_delay: 120
           (...)



## Pager Configuration

	# ----------------------
	# Pager services
	# ----------------------

	pagers:

	  general_pagername:         
	    type                : team_channel, teams, pagerduty (experimental), smtp(to be done)
	    mode                : managed(default), allnotifications
	    url                 : Teams channel URL, pagerduty URL
	    [enable]            : timerange 
	    [http_proxy]        : http://[login[:pass]@proxyhost:port  ; use noenv value to skip os/env     
	    [https_proxy]       : https://[login[:pass]]@proxyhost:port  ; default to http_proxy   
	    [http_code: 200]    : http_code for success
	    [ssl_verify: yes]   : default: no
        [rate_limit]        : seconds mini between alerts ; default 7200


	  myteams_ops:     
	     type               : teams
	     url                : https://client.webhook.office.com/webhookb2/XXXXXXX
	     mode               :
	     [enable]           : timerange


	  pagerduty_dev:
	     enable: yes                                   : timerange
	     type: pagerduty                               : pagerduty
	     mode: allnotifications :                      : managed/allnotifications 
	     url: https://events.pagerduty.com/v2/enqueue  : influx API URL
	     key: xxxxxxxxxxx                              : influx API key  (keep secret)
	     rate_limit: 5                                 : seconds mini between calls


##  Pager modes

In `managed mode`, CMT handles delay, up/down transitions, and rate-limit before firing an alert.

In `allnotifications`, CMT sends all raw alerts to remote Pagers which will be in charge of deduplication, rate-limit and proper human notification.
