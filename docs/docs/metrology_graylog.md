---
title:  Graylog for CMT
---

# Graylog metrology servers

## Graylog server configuration

You need to configure either :

* a GELF input over HTTP, say on port 8080
* a GELF input over UDP, say on port 12201

You can also add rsyslog and beats protocol to collect logfiles and various file oriented data (with filebeat)

## Graylog UDP GELF

    metrology_servers:
      graylog_test1:
          type: graylog_udp_gelf
          host: 10.10.10.13
          port: 12201
          send_rawdata: no
          rawdata_prefix: raw
          enable: yes

## Graylog HTTP GELF
      
    metrology_servers:
      graylog_test2:
          type: graylog_http_gelf
          url: http://10.10.10.13:8080/gelf
          [http_proxy: ...]              # http://[login[:pass]@proxyhost:port     
          [https_proxy: ...              # https://[login[:pass]]@proxyhost:port  ; default to http_proxy   
          [ssl_verify: yes]              # default: no
          [http_code: 200]               # http_code for success
          send_rawdata: no               # yes/no (default) : do we send multi-events (e.g. from mysqldata, or sendfile )
          rawdata_prefix: raw
          enable: yes

