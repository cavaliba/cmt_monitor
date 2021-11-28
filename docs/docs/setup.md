---
title: setup
---

# CMT setup and quickstart


## from a binary download

recommeded !

    $ curl http://www.cavaliba.com/download/cmt/cmt-XXXXX.bin
    $ sudo cp cmt-XXXXX.bin /usr/local/bin/cmt
    $ sudo chmod 755 /usr/local/bin/cmt


## from a github / zip download

* check prerequisite : python3.6+, 
* unzip to /opt/cmt/
* install requirements (pyaml, psutils, requests)

    python3 /opt/cmt/cmt.py


## Minimal configuration

    $ sudo mkdir /opt/cmt
    $ sudo vi /opt/cmt/conf.yml

        ---

        # minimal CMT  configuration
        # for CLI usage

        global:
          cmt_group: minidev
          cmt_node: minihost
          enable: yes

        load:
          my_load:
            enable: yes

## cli usage

        $ cmt --version
        $ cmt -s
        $ cmt --report
        $ cmt --help

## crontab

        # crontab -e
        * * * * * /usr/local/bin/cmt --cron >> /dev/null 2>&1

with forced proxy

        * * * * * export http_proxy=http://proxy:8080 ; /usr/local/bin/cmt --cron >> /dev/null 2>&1


## Next

* use CLI mode to test and configure
* use --available option to identify items to monitor
* watch for event in your elastic/graylog/kibana server
* deploy a larger configuration with various modules
* wakeup when the pager rings !