---
title: setup
---

# CMT setup 

## from a binary download


    $ curl http://www.cavaliba.com/download/cmt/cmt-XXXXX.bin
    $ sudo cp cmt-XXXXX.bin /usr/local/bin/cmt
    $ sudo chmod 755 /usr/local/bin/cmt



## from a github / zip download

* check prerequisite : python3.6+, 
* unzip to /opt/cmt/
* install requirements (pyaml, psutils, requests)

    python3 /opt/cmt/cmt.py


## Minimal configuration

    $ sudo mkdir /opt/cmt
    $ sudo vi /opt/cmt/conf.yml

        ---

        # minimal CMT 1.0 configuration
        # for CLI usage

        global:
          cmt_group: minidev
          cmt_node: minihost
          enable: yes

        #modules:
        #  load:
        #    enable: yes

        checks:
          my_load:
            module: load



## Next

* use CLI mode to test and configure
* use --available option to identify items to monitor
* configure crontab
* watch for event in your elastic/graylog/kibana server
