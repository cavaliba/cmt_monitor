---
title: configuration example
---


## Full configuration example

    ---
    # Cavaliba / cmt_monitor / conf.yml
    # CMT Version: 1.6


    # Example configuration / template 

    # Global section
    # --------------

    global:
      cmt_group: cavaliba
      cmt_node: vmxupm
      cmt_node_env: dev
      cmt_node_role: dev_cmt
      cmt_node_location: Ladig
      enable: yes
      enable_pager: yes
      conf_url: http://localhost/txt/
      pager_rate_limit: 3600
      max_execution_time: 55
      load_confd: yes
      alert_max_level: warn
      alert_delay: 90
      tags: global_tag1 global_tag2=value2


    # Metrology section
    # -----------------

    metrology_servers:

      graylog_test1:
          type: graylog_udp_gelf
          host: 10.10.10.13
          port: 12201
          enable: yes
      
      graylog_test2:
          type: graylog_http_gelf
          url: http://10.10.10.13:8080/gelf
          enable: yes

      elastic_test:
          type: elastic_http_json
          url: http://10.10.10.51:9200/cmt/data/?pipeline=timestamp
          enable: yes

      # CMT V1.7+ ; compatible with influxdb V1 & V2
      influxdb_test:
          type: influxdb
          # V1
          url: http://10.10.10.13:8086/write?db=cmt
          # V2
          # url: 
          # msec, sec, nsec ; anything else, no timestamp
          time_format: msec
          batch: yes
          token: toto
          #username: cmt
          #password : cmt
          enable: yes


    # Pager section
    # -------------

    pagers:

      alert:
        type: team_channel
        url: https://outlook.office.com/webhook/xxxxx/IncomingWebhook/yyyyyyyyyyyyyyy
        enable: yes

      test:
        type: team_channel
        url: https://outlook.office.com/webhook/xxxxx/IncomingWebhook/yyyyyyyyyyyyyyy
        enable: no

    # Modules section
    # ---------------

    modules:

    # SYNTAX
    #
    # modulename:
    #    enable            : timerange ; default yes
    #    [alert_max_level] : alert, warn, notice, none  (scale down)  ; overwrites global entry
    #    [alert_delay]     : delay before transition from to alert ; seconds/DEFAULT 120 
    #    [frequency]       : min seconds between runs ; needs --cron in ARGS


      load:
        enable: yes
        alert_max_level: notice

      cpu:
        enable: yes
      
      memory:
        enable: yes
        frequency: 600

      swap:
        enable: yes

      boottime:
        enable: yes

      ntp:
        enable: yes

      disk:
        enable: yes

      url:
        enable: yes

      mount:
        enable: yes
        alert_max_level: notice

      process:
        enable: yes

      ping:
        enable: yes
        alert_max_level: warn

      folder:
        enable: yes
        #alert_delay: 70
        #alert_max_level: alert
      
      certificate:
        enable: yes

      socket:
        enable: yes

      send:
        enable: yes


    # checks section
    # --------------

    # module_name:
    #
    #   checkname:
    #      [enable]           : timerange ; default yes ; yes, no, before, after, hrange, ho, hno
    #      [enable_pager]     : timerange ; default NO ; need global/pager to be enabled ; sent if alert found
    #      [alert_max_level]  : alert, warn, notice, none (scale down)  ; overwrites global & module entry
    #      [alert_delay]      : delay before transition from normal to alert (if alert) ; seconds  ; DEFAULT 120 
    #      [frequency]        : min seconds between runs ; needs --cron in ARGS ; overrides module config
    #      [root_required]    : [yes|no(default)] -  new 1.4.0 - is root privilege manadatory for this check ?
    #      [tags]             : tag1 tag2[=value] ... ; list of tags ; no blank space aroung optional "=value"
    #      arg1               : specific to module (see doc for each module)
    #      arg2               : specific to module  
    #      (...)


    load:
      myload:
        enable: yes
        alert_max_level: warn
        tags: local1 local2=43


    cpu:
      mycpu:
        enable: yes
        alert_max_level: alert


    memory:
      mymemory:
        enable: yes
        alert_max_level: alert
        frequency: 10


    boottime:
      myboottime:
        enable: yes
        alert_max_level: alert

    swap:
      myswap:
        enable: yes
        alert_max_level: alert


    disk:

      disk_root:
        path: /
        alert: 80

      disk_boot:
        path: /boot
        alert: 90


    url:

      www.cavaliba.com:
        enabled: after 2020-01-01
        url: https://www.cavaliba.com/
        pattern: "Cavaliba"
        allow_redirects: yes
        ssl_verify: yes
        #host: toto

      www_non_existing:
        enabled: after 2020-01-01
        url: http://www.nonexisting/
        #pattern: ""

      google:
        url: https://www.google.com/

      yahoo:
        url: https://www.yahoo.com/
        allow_redirects: yes
        ssl_verify: yes

      via_proxy_cavaliba:
        enabled: yes
        url: https://www.cavaliba.com/
        http_proxy: http://62.210.205.232:8080

      url_noenv_proxy:
        url: http://www.monip.org/
        http_proxy: noenv

      url_test_timeout:
        url: http://slowwly.robertomurray.co.uk/delay/4000/url/http://google.co.uk
        timeout: 2


    mount:

      mount_root:
        path: /

      mount_mnt:
        path: /mnt


    process:

      redis:
        psname: redis
        enable_pager: no

      apache:
        psname: httpd

      cron:
        psname: cron
        search_arg: "-f"
      
      ssh:
        psname: sshd

      ntp:
        psname: ntpd

      mysql:
        psname: mysqld

      php-fpm:
        psname: php-fpm
        enable_pager: yes


    ping:

      ping_vm1:
        host: 192.168.0.1

      ping_locahost:
        host: localhost

      www.google.com:
        host: www.google.com

      wwwtest:
        host: www.test.com    

      badname:
        host: www.averybadnammme_indeed.com  


    folder:

      dir_usrshare_doc:
        path: /usr/share/doc
        alert_max_level: none
        recursive: yes
        filter_extension: ".conf .hl7"

      dir_usrshare_doc2:
        path: /usr/share/doc
        alert_max_level: none
        recursive: yes
        filter_regexp: '^Makefile$'

      dir_usrshare_alsa:
        path: /usr/share/alsa
        alert_max_level: none
        recursive: yes
        filter_regexp: '.*.conf$'

      folder_mytmp:
        path: /tmp
        alert_max_level: alert
        #alert_delay: 30
        recursive: no
        target:
           is_blabla:
           #age_min: 1000
           #age_max: 300
           #files_min: 3
           #files_max: 10
           #size_min: 100000
           #size_max: 10
           has_files:
                - secret.pdf
                #- secret2.pdf

      folder_number2:
        path: /missing

      a_file:
        path: /tmp/ab.txt
        no_store: no

      folder_big_nostore:
        path: /usr/lib
        recursive: yes
        no_store: yes


    certificate:

      cert_google:
        hostname: google.com
        port: 443
        alert_in: 1 week 
        warning_in: 3 months
        notice_in: 6 months

      duck:
        hostname: duckduckgo.com
        alert_in: 1 week

      broken:
        hostname: duckduckgo.com
        port: 80
        alert_in: 2 week

      yahoo:
        hostname: yahoo.com
        port: 443
        alert_in: 2 week


    socket:

      redis:
        socket: local tcp 6379
        #socket: local tcp port | remote tcp host port
        connect: yes
        #send: 
        #pattern:

      www_google:
        socket: remote www.google.com tcp 443
        connect: yes
        #send: 
        #pattern:

    send:

        test_token1:
          attribute: test
          comment: "a test comment for token1 - cmt_test will be created in elastic"
          unit: "no_unit"


    #  -------------------------------------
    #  timerange field (from documentation)
    #  -------------------------------------
    #  - yes
    #  - no
    #  - after YYYY-MM-DD hh:mm:ss
    #  - before YYYY-MM-DD hh:mm:ss
    #  - hrange hh:mm:ss hh:mm:ss
    #  - ho   (8h30/18h mon>fri) - business hours
    #  - hno  (! (8h30/18h mon>fri)) - non business hours

    # ------------------------------------
    # conf.d/*.yml also included with :
    # - main conf has higher priority
    # - first level lists merged
    # ------------------------------------
