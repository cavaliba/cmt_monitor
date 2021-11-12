CAVALIBA - CMT Monitor 
======================

(c) Cavaliba.com 2020-2021  - Version 2.0 - 2021/11/12


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

phil@xu18:~/Bureau/dev/cmt_monitor$ vi /opt/cmt/conf.yml 
phil@xu18:~/Bureau/dev/cmt_monitor$ python3 cmt/cmt.py -s
------------------------------------------------------------
CMT - (c) cavaliba.com - Version 2.0 - 2021/11/12
------------------------------------------------------------
cmt_group      :  cavaliba
cmt_node       :  vmxupm
config file    :  /opt/cmt/conf.yml

OK       boottime     boot : 0 days since last reboot - 7:10:30 sec.
OK       load         load 1/5/15 min : 0.32  0.2  0.19
NOTICE   certificate  33 day(s) left for SSL certificate www.cavaliba.com:443
WARNING  certificate  58 day(s) left for SSL certificate google.com:443
OK       certificate  355 day(s) left for SSL certificate duckduckgo.com:443
CRITICAL certificate  no certificate found for duckduckgo.com:80
OK       certificate  68 day(s) left for SSL certificate yahoo.com:443
OK       cpu          cpu usage : 23.8 %
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
CRITICAL folder       test_age_max /opt/cmt/testdata : some files are too old (15651176 sec)
OK       folder       test_files_min /opt/cmt/testdata OK - 5 files, 6 dirs, 11004 bytes - targets 1/1
OK       folder       test_files_max /opt/cmt/testdata OK - 5 files, 6 dirs, 11004 bytes - targets 1/1
CRITICAL folder       test_size_min /opt/cmt/testdata : too small (11004)
CRITICAL folder       test_size_max /opt/cmt/testdata : too big (11004)
CRITICAL folder       test_has_recent /opt/cmt/testdata : missing young file (min 15651176 sec)
OK       folder       test_has_old /opt/cmt/testdata OK - 5 files, 6 dirs, 11004 bytes - targets 1/1
OK       folder       test_missing /opt/cmt/testdata/file.txt OK - 1 files, 0 dirs, 0 bytes - targets 0/0
OK       folder       test_nostore /opt/cmt/testdata/file.txt OK - 1 files, 0 dirs, 0 bytes [0.0 B] - targets 0/0

SKIPPED  module=folder check=folder_root : must run as root

OK       folder       folder_list /opt/cmt OK - 9 files, 7 dirs, 20234 bytes - targets 0/0
CRITICAL memory       memory above threshold : 82.4 % > 0.5 %
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
OK       process      process mysql found (mysqld, None) - memory rss 16.4 MB - cpu 4.51 sec.
CRITICAL process      process php-fpm missing (php-fpm, None)
OK       socket       socket local redis localhost tcp/6379 - alive: yes - count: 0
OK       socket       socket remote www_google www.google.com tcp/443 - alive: yes - count: 0
OK       swap         swap used: 6.8 % /  147.1 MB - total 2.1 GB
OK       url          url www.cavaliba.com - https://www.cavaliba.com/ [Host: ] - http=200 - 91 ms ; pattern OK
CRITICAL url          url www_non_existing - http://www.nonexisting/ [Host: ] - timeout/no response to query
OK       url          url google - https://www.google.com/ [Host: ] - http=200 - 95 ms ; pattern OK
OK       url          url yahoo - https://www.yahoo.com/ [Host: ] - http=200 - 611 ms ; pattern OK
OK       url          url via_proxy_cavaliba - https://www.cavaliba.com/ [Host: ] - http=200 - 83 ms ; pattern OK
OK       url          url url_noenv_proxy - http://www.monip.org/ [Host: ] - http=200 - 69 ms ; pattern OK
CRITICAL url          url url_test_timeout - http://slowwly.robertomurray.co.uk/delay/4000/url/http://google.co.uk [Host: ]- bad http code response (404 received, expected 200)
OK       url          url url_auth - https://monitor.kheops.ch/kibana [Host: ] - http=200 - 231 ms ; pattern OK
OK       url          url url_httpcode - https://monitor.kheops.ch/kibana [Host: ] - http=401 - 137 ms ; pattern OK
CRITICAL url          url url_patternreject : forbidden pattern found in https://monitor.kheops.ch (Host: )

SKIPPED  module=send check=test_token1 : 

OK       sendfile     /opt/cmt/demo.json - 3 lines/events
OK       mysqldata    db_query1 - 2 lines collected

2021/11/12 - 18:09:56 : SEVERITY=CRITICAL - 58 checks - 39 ok - 19 nok - 16 criticial - 0 error - 2 warning - 1 notice.


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

