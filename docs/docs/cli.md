---
title: CLI
---

# CMT used in command-line mode (CLI)

If cmt is deployed as a binary (recommended):

   $ cmt
   $ cmt -s          # standard checks, short output
   $ sudo cmt -s     # to include checks requesting elevated privileges

If cmt is deployed as python source files :

    $ python3 /my/dir/to/cmt.py 

## help

    $ cmt --help

    usage: cmt.py [-h] [--cron] [--report] [--pager] [--persist] [--conf CONF]
                  [--listmodules] [--available] [--pagertest]
                  [--no-pager-rate-limit] [--checkconfig] [--version] [--debug]
                  [--debug2] [--devmode] [--short] [--check CHECK]
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
      --check CHECK         check name for single check run
 

## Full run, short output (-s)

    $ ./cmt.py -s

    ------------------------------------------------------------
    CMT - Version 1.0.0 - (c) Cavaliba.com - 2020/11/29
    ------------------------------------------------------------
    2020/11/29 - 15:59:08 : Starting ...
    cmt_group      :  cavaliba
    cmt_node       :  vmxupm

    Short output
    ------------

    OK      load       1/5/15 min : 0.44  0.46  0.53
    OK      cpu        usage : 10.8 %
    OK      memory     used 85.2 % - used 2.0 GB - avail 406.8 MB - total 2.7 GB
    OK      boottime   days since last reboot : 0 days - 23:35:57 sec.
    OK      swap       used: 13.9 % /  297.4 MB - total 2.1 GB
    OK      disk       path : / - used: 32.4 % - used: 20.7 GB - free: 43.2 GB - total: 67.4 GB 
    OK      disk       path : /boot - used: 32.4 % - used: 20.7 GB - free: 43.2 GB - total: 67.4 GB 
    OK      url        www.cavaliba.com - https://www.cavaliba.com/ [Host: ] - http=200 - 103 ms ; pattern OK
    NOK     url        www_non_existing - http://www.nonexisting/ [Host: ] - no response to query
    OK      mount      path / found
    NOTICE  mount      path /mnt not found
    NOK     process    redis missing (redis)
    NOK     process    apache missing (httpd)
    OK      process    cron found (cron) - memory rss 2.9 MB - cpu 0.04 sec.
    OK      process    ssh found (sshd) - memory rss 3.9 MB - cpu 0.05 sec.
    NOK     process    ntp missing (ntpd)
    OK      process    mysql found (mysqld) - memory rss 56.3 MB - cpu 20.83 sec.
    NOK     process    php-fpm missing (php-fpm)
    OK      ping       192.168.0.1 ok
    OK      ping       localhost ok
    OK      ping       www.google.com ok
    WARN    ping       www.test.com not responding
    WARN    ping       www.averybadnammme_indeed.com not responding
    NOK     folder     /tmp : expected file not found (secret.pdf)
    NOK     folder     /missing missing
    NOTICE  mount      path /merge not found
    OK      url        demo.cavaliba.com - http://demo.cavaliba.com/ [Host: ] - http=200 - 181 ms ; pattern OK

    Notification Summary
    --------------------

    Notice 
    mount           : path /mnt not found
    mount           : path /merge not found

    Warnings 
    ping            : www.test.com not responding
    ping            : www.averybadnammme_indeed.com not responding

    Alerts 
    url             : www_non_existing - http://www.nonexisting/ [Host: ] - no response to query
    process         : redis missing (redis)
    process         : apache missing (httpd)
    process         : ntp missing (ntpd)
    process         : php-fpm missing (php-fpm)
    folder          : /tmp : expected file not found (secret.pdf)
    folder          : /missing missing

    2020/11/29 - 15:59:12 : Done.


## Limit to some module

    $ ./cmt.py process load memory


## Limit to a specific check

    $ ./cmt.py --check mycheckname


## Send reports to metrology (force in CLI mode)

  $ cmt --report


## devmode (output reports to terminal - no real report send to metrology)

  $ cmt -s --report --devmode

  