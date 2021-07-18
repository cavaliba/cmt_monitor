---
title: Home
---

# Welcome to CMT Documentation

*Current release : 1.8.1 - 2021/07/18*

## Overwiew - CMT is a simple monitoring agent

CMT is a small footprint agent, with a single file configuration, available for most standard Linux OS. Once deployed on a system, it collects various data and monitors local/remote services. 

## Send to ElasticSearch/InfluxDB/Graylog

Collected data is sent to Metrology servers like ElasticSearch, InfluxDB V1/V2 or Graylog. These data points may carry alert information or warning levels for central alerting or display (Kibana for example).

## Alerts and Pager to Teams

If various conditions are met (or not met), CMT can also send direct alerts / pagers notifications to Teams channel.

## Use as CLI

For sysadmin, CMT can be used as command line tool on each server during various sysadmin or software configuration tasks. One single run provides an immediate health check of all the configured check items.


    $ cmt -s

    ------------------------------------------------------------
    CMT - (c) cavaliba.com - Version 1.8.1 - 2021/07/18
    ------------------------------------------------------------
    cmt_group      :  cavaliba
    cmt_node       :  vmxupm2
    config file    :  /opt/cmt/conf.yml

    OK      boottime     boot : 0 days since last reboot - 20:36:47 sec.
    OK      load         load 1/5/15 min : 0.79  0.59  0.49
    WARN    certificate  58 day(s) left for SSL certificate google.com:443
    OK      certificate  130 day(s) left for SSL certificate duckduckgo.com:443
    NOK     certificate  no certificate found for duckduckgo.com:80
    NOTICE  certificate  37 day(s) left for SSL certificate yahoo.com:443
    OK      cpu          cpu usage : 11.3 %
    OK      disk         disk / - used: 42.8 % - used: 27.3 GB - free: 36.6 GB - total: 67.4 GB 
    OK      disk         disk /boot - used: 42.8 % - used: 27.3 GB - free: 36.6 GB - total: 67.4 GB 
    OK      folder       test_extension /opt/cmt/testdata OK - 2 files, 5 dirs, 0 bytes - targets 0/0
    OK      folder       test_regexp /opt/cmt/testdata OK - 2 files, 5 dirs, 0 bytes - targets 0/0
    OK      folder       test_regexp_ext /opt/cmt/testdata OK - 1 files, 5 dirs, 0 bytes - targets 0/0
    WARN    folder       test_wrong_target /opt/cmt/testdata : unknown target is_blabla
    OK      folder       test_hasfile /opt/cmt/testdata OK - 6 files, 5 dirs, 11004 bytes - targets 1/1
    OK      folder       test_age_min /opt/cmt/testdata OK - 6 files, 5 dirs, 11004 bytes - targets 1/1
    NOK     folder       test_age_max /opt/cmt/testdata : some files are too old (8983776 sec)
    OK      folder       test_files_min /opt/cmt/testdata OK - 6 files, 5 dirs, 11004 bytes - targets 1/1
    OK      folder       test_files_max /opt/cmt/testdata OK - 6 files, 5 dirs, 11004 bytes - targets 1/1
    NOK     folder       test_size_min /opt/cmt/testdata : too small (11004)
    NOK     folder       test_size_max /opt/cmt/testdata : too big (11004)
    NOK     folder       test_has_recent /opt/cmt/testdata : missing young file (min 7864049 sec)
    OK      folder       test_has_old /opt/cmt/testdata OK - 6 files, 5 dirs, 11004 bytes - targets 1/1
    OK      folder       test_missing /opt/cmt/testdata/file.txt OK - 1 files, 0 dirs, 0 bytes - targets 0/0
    OK      folder       test_nostore /opt/cmt/testdata/file.txt OK - 1 files, 0 dirs, 0 bytes [0.0 B] - targets 0/0
    OK      memory       mem used 80.7 % - used 1.9 GB - avail 530.9 MB - total 2.7 GB
    OK      mount        mount / found
    NOTICE  mount        mount /mnt not found
    OK      ping         ping 192.168.0.1 ok
    OK      ping         ping localhost ok
    OK      ping         ping www.google.com ok
    WARN    ping         ping www.test.com not responding
    WARN    ping         ping www.averybadnammme_indeed.com not responding
    NOK     process      process redis missing (redis, None)
    NOK     process      process apache missing (httpd, None)
    OK      process      process cron found (cron, None) - memory rss 2.6 MB - cpu 0.02 sec.
    OK      process      process ssh found (sshd, None) - memory rss 2.9 MB - cpu 0.05 sec.
    NOK     process      process ntp missing (ntpd, None)
    OK      process      process mysql found (mysqld, None) - memory rss 146.2 MB - cpu 22.64 sec.
    NOK     process      process php-fpm missing (php-fpm, None)
    OK      socket       socket local redis localhost tcp/6379 - alive: yes - count: 0
    OK      socket       socket remote www_google www.google.com tcp/443 - alive: yes - count: 0
    OK      swap         swap used: 15.2 % /  325.6 MB - total 2.1 GB
    OK      url          url www.cavaliba.com - https://www.cavaliba.com/ [Host: ] - http=200 - 769 ms ; pattern OK
    NOK     url          url www_non_existing - http://www.nonexisting/ [Host: ] - timeout/no response to query
    OK      url          url google - https://www.google.com/ [Host: ] - http=200 - 395 ms ; pattern OK
    OK      url          url yahoo - https://www.yahoo.com/ [Host: ] - http=200 - 1045 ms ; pattern OK
    OK      mysql        mydbmaster - cx=2 cx/s=0 r/s=0 w/s=0 q/s=0 mem=276053016
    OK      mysql        mydbslave - slave 0 sec. behind (limit = 180) - cx=1 cx/s=0 r/s=0 w/s=0 q/s=0 mem=277515936

    2021/07/18 - 14:49:38 : Done - 48 checks - 32 ok - 16 nok - 10 alerts - 4 warning - 2 notice.


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
        cmt*.py         # python3 version if pure python code prefered
        checks/*.py     # modular checks (idem)
        conf.yml        # configuration what to measure / where to send
        conf.d/         # additional configuration (eg. ansible additive deployment)
        persist.json    # optional data persistance across run (crontab mode mostly)

## Why another monitoring tool ?

The initial requirements were :

* small footprint agent, easy to deploy (drop anywhere ...)
* clean metric data structure (multi-tenant, multi-customers, multi nodes)
* simple configuration file (one for all)
* data agnostic: technical, business, ...
* push rather than pull : push data to metrology servers
* data is sent to very standard ElasticSearch / INfluxDB DataStore, private or in the cloud
* modular design for easy extension / additional checks or modules
* minimal learning curve : drop the binary, edit the conf, run as cron/CLI, send to Elasticsearch, create Dashboard.
* ansible aware for mass deployement and standardization
* usable as CLI directly on each system
* open source and hopefully well documented enough

None of the reviewed tools covered this exact set of requirements, some being too specific on technical metrics, others requiring a steep learning curve (eg. to extend), other used specific datastore and needed very specific protocol to be allowed (network/firewalls) between agents and datastore ...


## Enjoy

CMT is free to use, free to extend. Experiment, Adopt, Enjoy, Contribute.

