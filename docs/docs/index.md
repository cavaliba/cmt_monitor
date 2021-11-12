---
title: Home
---

# Welcome to CMT Documentation

*Current release : 2.0 - 2021/11/12*

## Overwiew - CMT is a simple monitoring agent

CMT is a small footprint agent, with a single file configuration, available for most standard Linux OS. Once deployed on a system, it collects various data and monitors local/remote services. 

## Send to ElasticSearch/InfluxDB/Graylog

Collected data is sent to Metrology servers like ElasticSearch, InfluxDB V1/V2 or Graylog. These data points may carry alert information or warning levels for central alerting or display (Kibana for example).

## Alerts and Pager to Teams and PagerDuty

If various conditions are met (or not met), CMT can also send direct alerts / pagers notifications to Teams channel.

## Use as CLI

For sysadmin, CMT can be used as command line tool on each server during various sysadmin or software configuration tasks. One single run provides an immediate health check of all the configured check items.

    $ cmt -s

    ------------------------------------------------------------
    CMT - (c) cavaliba.com - Version 2.0 - 2021/11/12
    ------------------------------------------------------------
    cmt_group      :  cavaliba
    cmt_node       :  vmxupm
    config file    :  /opt/cmt/conf.yml

    OK       boottime     boot : 0 days since last reboot - 7:07:49 sec.
    OK       load         load 1/5/15 min : 0.13  0.18  0.19
    NOTICE   certificate  33 day(s) left for SSL certificate www.cavaliba.com:443
    WARNING  certificate  58 day(s) left for SSL certificate google.com:443
    OK       certificate  355 day(s) left for SSL certificate duckduckgo.com:443
    CRITICAL certificate  no certificate found for duckduckgo.com:80
    OK       certificate  68 day(s) left for SSL certificate yahoo.com:443
    OK       cpu          cpu usage : 14.6 %
    OK       disk         disk / - used: 24.1 % - used: 15.5 GB - free: 48.6 GB - total: 67.6 GB 
    OK       disk         disk /boot - used: 24.1 % - used: 15.5 GB - free: 48.6 GB - total: 67.6 GB 
    OK       folder       test_recursive100 /opt/cmt/testdata/arbo100 OK - 100 files, 10 dirs, 0 bytes - targets 0/0
    OK       folder       test_extension /opt/cmt/testdata OK - 2 files, 16 dirs, 0 bytes - targets 0/0
    OK       folder       test_regexp /opt/cmt/testdata OK - 2 files, 16 dirs, 0 bytes - targets 0/0
    OK       folder       test_regexp_no_recurse /opt/cmt/testdata OK - 1 files, 6 dirs, 0 bytes - targets 0/0
    OK       folder       test_regexp_ext /opt/cmt/testdata OK - 1 files, 16 dirs, 0 bytes - targets 0/0
    WARNING  folder       test_wrong_target /opt/cmt/testdata : unknown target is_blabla
    OK       folder       test_hasfile /opt/cmt/testdata OK - 5 files, 6 dirs, 11004 bytes - targets 1/1
    OK       folder       test_age_min /opt/cmt/testdata OK - 5 files, 6 dirs, 11004 bytes - targets 1/1
    CRITICAL folder       test_age_max /opt/cmt/testdata : some files are too old (15651015 sec)
    OK       folder       test_files_min /opt/cmt/testdata OK - 5 files, 6 dirs, 11004 bytes - targets 1/1
    OK       folder       test_files_max /opt/cmt/testdata OK - 5 files, 6 dirs, 11004 bytes - targets 1/1
    CRITICAL folder       test_size_min /opt/cmt/testdata : too small (11004)
    CRITICAL folder       test_size_max /opt/cmt/testdata : too big (11004)
    CRITICAL folder       test_has_recent /opt/cmt/testdata : missing young file (min 15651015 sec)
    OK       folder       test_has_old /opt/cmt/testdata OK - 5 files, 6 dirs, 11004 bytes - targets 1/1
    OK       folder       test_missing /opt/cmt/testdata/file.txt OK - 1 files, 0 dirs, 0 bytes - targets 0/0
    OK       folder       test_nostore /opt/cmt/testdata/file.txt OK - 1 files, 0 dirs, 0 bytes [0.0 B] - targets 0/0

    SKIPPED  module=folder check=folder_root : must run as root

    OK       folder       folder_list /opt/cmt OK - 9 files, 7 dirs, 20234 bytes - targets 0/0
    CRITICAL memory       memory above threshold : 79.8 % > 0.5 %
    OK       mount        mount / found
    CRITICAL mount        mount /mnt not found
    OK       ping         ping 192.168.0.1 ok
    OK       ping         ping localhost ok
    OK       ping         ping www.google.com ok
    CRITICAL ping         ping www.test.com not responding
    CRITICAL ping         ping www.averybadnammme_indeed.com not responding
    CRITICAL process      process redis missing (redis, None)
    CRITICAL process      process apache missing (httpd, None)
    OK       process      process cron found (cron, -f) - memory rss 3.1 MB - cpu 0.01 sec.
    OK       process      process ssh found (sshd, None) - memory rss 4.9 MB - cpu 0.04 sec.
    CRITICAL process      process ntp missing (ntpd, None)
    OK       process      process mysql found (mysqld, None) - memory rss 16.4 MB - cpu 4.49 sec.
    CRITICAL process      process php-fpm missing (php-fpm, None)
    OK       socket       socket local redis localhost tcp/6379 - alive: yes - count: 0
    OK       socket       socket remote www_google www.google.com tcp/443 - alive: yes - count: 0
    OK       swap         swap used: 6.7 % /  143.4 MB - total 2.1 GB
    CRITICAL url          url www.cavaliba.com : forbidden pattern found in https://www.cavaliba.com/ (Host: )
    CRITICAL url          url www_non_existing - http://www.nonexisting/ [Host: ] - timeout/no response to query
    CRITICAL url          url google : forbidden pattern found in https://www.google.com/ (Host: )
    CRITICAL url          url yahoo : forbidden pattern found in https://www.yahoo.com/ (Host: )
    CRITICAL url          url via_proxy_cavaliba : forbidden pattern found in https://www.cavaliba.com/ (Host: )
    CRITICAL url          url url_noenv_proxy : forbidden pattern found in http://www.monip.org/ (Host: )
    CRITICAL url          url url_test_timeout - http://slowwly.robertomurray.co.uk/delay/4000/url/http://google.co.uk [Host: ]- bad http code response (404 received, expected 200)
    CRITICAL url          url url_auth : forbidden pattern found in https://monitor.kheops.ch/kibana (Host: )
    CRITICAL url          url url_httpcode : forbidden pattern found in https://monitor.kheops.ch/kibana (Host: )
    CRITICAL url          url url_patternreject : forbidden pattern found in https://monitor.kheops.ch (Host: )

    SKIPPED  module=send check=test_token1 : 

    OK       sendfile     /opt/cmt/demo.json - 3 lines/events
    OK       mysqldata    db_query1 - 2 lines collected

    2021/11/12 - 18:07:16 : SEVERITY=CRITICAL - 58 checks - 32 ok - 26 nok - 23 criticial - 0 error - 2 warning - 1 notice.




## Data model / data storage

CMT provides a clean and well organized  data model to enable an efficient metrology storage and further processing of collected data. You can then build various dashborad for data analysis and correlation,  for reporting, finer alerting, etc.


## Deploy easily

CMT is provided as a standalone binary for most recent linux distributions. Download and get running. Optionnaly yon can download and run directly the python3 code with a few mandatory librairies (yaml, requests, psutils, ...)

## Modular

Ultimately, due to its simple configuration and modular design, it is very easy to add new checks or new modules, thus enabling a single tool to cover technical and functionnal monitoring and alerting needs.

## Command and shortcuts

* `cmt --help`
* (...)

## CMT remote management

CMT optionally supports additional configuration items from a remote URL, downloaded at runtime. It enables various modification from a central server (enable or disable some modules and check, require additional checks, ...). 

No assumption is made on the remote server providing additional configuration. It can be as simple as text files from a shared Web server. It can also be an API to your existing systems which have to respond for a given CMT node, 
with a slice of configuration to be merged in the node's local configuration.


## Modules and Checks

Think of module has class of check for a specific family of items,  like URL, folder, process, disk... Modules are internally implemented as small  python file in the checks/ folder.

Checks are instance of module execution. Each check create one metrology message or event. A check can carry several datapoint (checkitems). Each checks carries optionnal alert,warning, notice information and a message formatted for human reading.

Each Check depending on his Module capacbilities can set information such as alert, warning, notice that will be sent back to metrology servers and possibly direct Pagers services.

Pager notifications are sent only once per CMT exectuion at most. It is intended for (very) standalone usage of CMT, 
whereas advanced usage with many nodes will benefit from Pager notification fired from central systms where
decisions can be made from many/all monitoring sources.

CMT provides various configuration to ease configuring alert levels, frequency, rate-limit, max level,  threshold, and other **stop switches** to garantee a clean thread of monitoring data to Metrology servers and Pagers.


## CMT automated run from crontab

CMT is intended to run from crontab, every minute. It has a built-in max-duration security to prevent unfinished 
executing to overcrowd a server.

## Deployment layout

    /usr/local/bin/cmt  # binary standalone

    /opt/cmt            # Home dir
        cmt             # cmt binary agent if prefered over /usr/local/bin
        mysql.cnf       # credentials for mysql checks if needed
        conf.yml        # configuration what to measure / where to send
        conf.d/         # additional configuration (eg. ansible additive deployment)
        persist.json    # optional data persistance across run (crontab mode mostly)

## Why another monitoring tool ?

The initial requirements were :

* small footprint agent, easy to deploy (drop anywhere ...)
* usable both with CRON and as interactive/CLI directly on each system
* clean metric data structure (multi-tenant, multi-customers, multi nodes)
* simple configuration file (one for all)
* data agnostic: technical, business, ...
* push rather than pull : push data to metrology servers
* data is sent to very standard ElasticSearch / INfluxDB DataStore, private or in the cloud
* modular design for easy extension / additional checks or modules
* minimal learning curve : drop the binary, edit the conf, run as cron/CLI, send to Elasticsearch, create Dashboard.
* ansible aware for mass deployement and standardization
* open source and hopefully well documented enough

None of the reviewed tools covered this exact set of requirements, some being too specific on technical metrics, others requiring a steep learning curve (eg. to extend), other used specific datastore and needed very specific protocol to be allowed (network/firewalls) between agents and datastore ...


## Enjoy

CMT is released under BSD-3clause licence, free to use, free to extend. Experiment, Adopt, Enjoy, Contribute.

