---
title: check_send
---

# Check: sendfile

*new in 2.0*


**sendfile** is a  module which takes a json file as parameter, and sends it to metrology servers


## Use case


This module is useful if some external systems produces outputs as json results whihc have to be sent to metrology servers for operations , display, alerting.  

E.g. : SQL requests, webservices output, external scripts, etc.


## Create a check entry 

    sendfile:
        mysendfile:
            jsonfile: /opt/cmt/demo.json
            frequency: 3600


## JSON example

    $ cat /opt/cmt/demo.json 

    [
    { "user":"fred", "last-login-days":4 },
    { "user":"jack", "last-login-days":7 },
    { "user":"igor", "last-login-days":9 }
    ]


## JSON expected format 

Expected json is an array (list) of dictionary (hash) like this

    [ 
        {"key1":value1, "key2":value2] ... },
        {"key1":value1, "key2":value2] ... },
        {"key1":value1, "key2":value2] ... },
        {"key1":value1, "key2":value2] ... }
    ]

Keys don't need to be the same accross each dictionary.

## Events

One **global event**  is sent for each sendfile  check in the configuration with :

    cmt_sendfile_name        /opt/cmt/demo.json
    cmt_sendfile_lines       3

    and all the usual attributes cmt_node,groupe,id, check, module, message...

One or more **data events** are sent for each line/dictionary in the json file with :

    Each key created by appending cmt_sendfile_  before the json key name.
    An additional attribute is sent : cmt_multievent_id  (line count)


Thus json 

    [ "key1":value1, "key2":value2] ...
    
will produce one data event 

    cmt_sendfile_key1: value1
    cmt_sendfile_key2: value2
    ...

and json:

    [ 
        {"key1":value1, "key2":value2] ... },
        {"key1":value1, "key2":value2] ... },
        {"key1":value1, "key2":value2] ... },
        {"key1":value1, "key2":value2] ... }
    ]
    
will produce 4 data events with each : 
 
    cmt_sendfile_key1: value1
    cmt_sendfile_key2: value2
    ...



