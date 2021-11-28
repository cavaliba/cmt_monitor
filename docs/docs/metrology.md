---
title:  Introduction to Metrology servers for CMT
---

# Metrology for CMT

CMT can send data to metrology servers, when run from cron `--cron` or with the `--report` option.


## Supported remote servers

CMT can send data to:

* ElasticSearch 6 / 7 with standard json over HTTP (since CMT version 1.6)
* InfluxDB V1/V2 starting with cmt 1.7+ ; line protocol over HTTP
* Graylog 2 or 3 with a GELF connector over HTTP protocol
* Graylog 2 or 3 with a GELF connector over UDP network protocol

SSL/TLS (HTTPS) URLs can be configured instead of clear HTTP.


HTTP protocol is a TCP-connected protocol. If the remote server is slow or unavailable, CMT will detect and prevent any slowdown by cancelling data transfer for the run.

UDP protocol has the main advantage to not require a network connection from CMT agent to remote server. It's fire and forget. But it is not always available across network boundaries and firewalls.

Proxy configuration to reach HTTP/HTTPS targes is supported globally and per metrology target. It includes options for expliciting http_proxy, https_proxy, verification or not of target SSL certificates (default is yes). You can pass a `noenv` http_proxy value to ignore OS environment proxy.


## Which remote server is better ?

If unsure go with Graylog 3. It provides an all-included log aggregation system also based on an underlying Elasticsearch storage. The configuration is easy with a clean Web user interface. It helps manage protocols/connectors (inputs), index rotation, authentication, dashboard, alerts, etc. all from that simple and nice UI. Graylog has a narrower audience than Elastic. You can add Kibana later on top of your underlying Elasticsearch. You can even display Elasticdata from Grafana.

ElasticSearch is one of the most popular NoSQL datastore. It's a great choice as you may already have an available Elasticsearch server running in your systems. You'll need Kibana for powerful vizualisation and you'll have to configure index and alias creation, index rotation ... 

InfluxDB is easy to setup, and can provide very adequate Visulization (Grafana), Dashboards and Alerting. It is better suited for numerical data / time series.

You can specify multiple metrology servers in the configuration. They will all receive all the collected data.


## rawdata

Some CMT modules can perform database queries or parse existing files (json) and send the data to metrology servers. Each line of the response is sent as a separate message (rawdata/multi-event).

    metrology_targetXX:  
      (...)
      send_rawdata: no         # decide if you want raw data sent to this target
      rawdata_prefix: raw      # optionally choose a preix for field names

Graylog and Elastic are good candidates to receive rawdata. 

InfluxDB is not suited for rawdata. These kind of raw data can create a high cardinality not suitable for time series database.
