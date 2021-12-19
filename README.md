CAVALIBA - CMT Monitor 
======================

(c) Cavaliba.com 2020-2021  - Version 2.2 - 2021/12/19


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

    usage: cmt [-h] [--version] [--short] [--cron] [--check CHECK] [--conf CONF]
           [--report] [--persist] [--listmodules] [--available]
           [--pager_enable] [--pager_test] [--no-pager-rate-limit]
           [--pager [PAGER [PAGER ...]]] [--nopersist] [--checkconfig]
           [--debug] [--debug2] [--devmode]
           [modules [modules ...]]


    (...)


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
    OK       cpu          cpu usage : 14.6 %
    OK       disk         disk / - used: 24.1 % - used: 15.5 GB - free: 48.6 GB - total: 67.6 GB 
    OK       disk         disk /boot - used: 24.1 % - used: 15.5 GB - free: 48.6 GB - total: 67.6 GB 
    OK       folder       test_recursive100 /opt/cmt/testdata/arbo100 OK - 100 files, 10 dirs, 0 bytes - targets 0/0
    OK       folder       test_extension /opt/cmt/testdata OK - 2 files, 16 dirs, 0 bytes - targets 0/0
    (...)
    CRITICAL url          url url_patternreject : forbidden pattern found in https://test.demo.com (Host: )
    OK       sendfile     /opt/cmt/demo.json - 3 lines/events
    OK       mysqldata    db_query1 - 2 lines collected

    2021/11/12 - 18:07:16 : SEVERITY=CRITICAL - 58 checks - 32 ok - 26 nok - 23 criticial - 0 error - 2 warning - 1 notice.

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

