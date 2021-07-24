CAVALIBA - CMT Monitor 
======================

(c) Cavaliba.com 2020-2021  - Version 1.8.2 - 2021/07/24


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
      -  mysql


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

