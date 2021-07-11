CAVALIBA - CMT Monitor 
======================

(c) Cavaliba.com 2020-2021  - Version 1.8beta - 2021/07/11


CMT Monitor is a simple software agent to :

* collect standard OS, Middleware, Network ... and Custom metrics
* check application status and remote URLs  for response and pattern
* send alerts to Pager (Teams channels)
* send data to Metrology servers (Elastic/Graylog/InfluxDB) for additional reporting and alerting
* help troubleshoot outage when run as CLI (interactive : cmt -s)
* easy one-file configuration
* easy automation and deployment with Ansible-like tools.


download standalone binary
--------------------------

    http://www.cavaliba.com/download/cmt/
    sudo cp cmt-XX.bin /usr/local/bin/cmt
    sudo chmod 755 /usr/local/bin/cmt
    cmt --version

get source from github if needed
---------------------------------

    git clone https://github.com/cavaliba/cmt_monitor.git

read the documentation
----------------------

    http://www.cavaliba.com/cmt/doc/index.html


see help
--------

    $ ./cmt.py --help

    usage: cmt.py [-h] [--cron] [--report] [--pager] [--persist] [--conf CONF]
                  [--listmodules] [--available] [--pagertest]
                  [--no-pager-rate-limit] [--checkconfig] [--version] [--debug]
                  [--debug2] [--devmode] [--short]
                  [modules [modules ...]]

    CMT - Cavaliba Monitoring

    positional arguments:
      modules               modules to check

    optional arguments:
      -h, --help            show this help message and exit
      --cron                equiv to report, alert, persist, short output
      --report              send events to Metrology servers
      --pager               send alerts to Pagers
      --persist             persist data accross CMT runs (use in cron)
      --conf CONF           specify alternate yaml config file
      --listmodules         display available modules
      --available           display available entries found for modules (manual
                            run on target)
      --pagertest           send test message to teams and exit
      --no-pager-rate-limit
                            disable pager rate limit
      --checkconfig         checkconfig and exit
      --version, -v         display current version
      --debug               verbose/debug output
      --debug2              more debug
      --devmode             dev mode, no pager, no remote metrology
      --short, -s           short compact cli output


CLI - run manually
------------------

      $ cmt -s

      ------------------------------------------------------------
      CMT - (c) cavaliba.com - Version 1.6.1 - 2021/04/18
      ------------------------------------------------------------
      cmt_group      :  cavaliba
      cmt_node       :  vmxupm2
      config file    :  /opt/cmt/conf.yml

      OK      boottime     boot : 0 days since last reboot - 0:51:56 sec.
      OK      load         load 1/5/15 min : 0.25  0.22  0.2
      WARN    certificate  57 day(s) left for SSL certificate google.com:443
      OK      certificate  205 day(s) left for SSL certificate duckduckgo.com:443
      NOK     certificate  no certificate found for duckduckgo.com:80
      OK      certificate  128 day(s) left for SSL certificate yahoo.com:443
      OK      cpu          cpu usage : 3.8 %
      OK      disk         disk / - used: 41.8 % - used: 26.7 GB - free: 37.2 GB - total: 67.4 GB 
      OK      disk         disk /boot - used: 41.8 % - used: 26.7 GB - free: 37.2 GB - total: 67.4 GB 
      NOK     folder       folder /tmp : expected file not found (secret.pdf)
      OK      folder       folder folder_bad_target (/tmp) OK - 3 files, 16 dirs, 425 bytes - targets 0/1
      NOK     folder       folder /missing missing
      NOK     folder       folder /tmp/ab.txt missing
      NOK     folder       folder /tmp/ab.txt missing
      OK      folder       folder folder_big_nostore (/usr/lib) OK - 20881 files, 2040 dirs, 2630640432 bytes [2.6 GB] - targets 0/0
      OK      memory       mem used 54.9 % - used 1.2 GB - avail 1.2 GB - total 2.7 GB
      OK      mount        mount / found
      NOTICE  mount        mount /mnt not found
      OK      ping         ping 192.168.0.1 ok
      OK      ping         ping localhost ok
      OK      ping         ping www.google.com ok
      WARN    ping         ping www.test.com not responding
      WARN    ping         ping www.averybadnammme_indeed.com not responding
      NOK     process      process redis missing (redis, None)
      NOK     process      process apache missing (httpd, None)
      OK      process      process cron found (cron, None) - memory rss 3.0 MB - cpu 0.0 sec.
      OK      process      process ssh found (sshd, None) - memory rss 5.6 MB - cpu 0.01 sec.
      NOK     process      process ntp missing (ntpd, None)
      OK      process      process mysql found (mysqld, None) - memory rss 90.2 MB - cpu 0.68 sec.
      NOK     process      process php-fpm missing (php-fpm, None)
      OK      socket       socket local redis localhost tcp/6379 - alive: yes - count: 0
      OK      socket       socket remote www_google www.google.com tcp/443 - alive: yes - count: 0
      OK      swap         swap used: 0.1 % /  1.3 MB - total 2.1 GB
      OK      url          url www.cavaliba.com - https://www.cavaliba.com/ [Host: ] - http=200 - 98 ms ; pattern OK
      NOK     url          url www_non_existing - http://www.nonexisting/ [Host: ] - timeout/no response to query
      OK      url          url google - https://www.google.com/ [Host: ] - http=200 - 99 ms ; pattern OK
      OK      url          url yahoo - https://www.yahoo.com/ [Host: ] - http=200 - 691 ms ; pattern OK

      2021/04/18 - 13:54:44 : Done - 37 checks - 23 ok - 14 nok - 10 alerts - 3 warning - 1 notice.

crontab
-------

    $ sudo crontab -e

    */2 * * * * /usr/local/bin/cmt --cron


Available Modules
-----------------

    $ ./cmt.py --listmodule

      -  load
      -  cpu
      -  memory
      -  swap
      -  boottime
      -  mount
      -  disk
      -  url
      -  process
      -  ping
      -  folder
      -  certificate
      -  socket
      -  send


REFERENCE
---------
See included file docs/

LICENSE
-------
See LICENSE file. Opensurce Software with a 3 points BDS-like license.

SUPPORT
-------
CMT is provided as-is and no direct support is available at the moment. 
Feel free to drop a note at contact@cavaliba.com anyway.

RELEASE
--------
see docs/version.md


COPYRIGHT
---------

    (c) Cavaliba.com - 2020-2021

