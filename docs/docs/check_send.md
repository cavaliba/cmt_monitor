---
title: check_send
---

# Check: Send

*new in 1.4.0*


**Send** is a specific module which takes a value on STDIN and pipe it to CMT for immediate send.


## Use case


    echo "42" | cmt send --check mytestcheck --report

    date | python3 /opt/cmt/cmt.py --conf conf.yml send --check mytestcheck --report



## Caveat 

This module has a specific behavior since it must be the only one to be executed during a single run, 
with explicit modulename (send) and checkname (--check checkname) on the command line arguments.

It is not exectuted when cmt is run globally with many or all modules and checks.

It needs a configuration entry to map the  received value from STDIN to an attribute sent to metrology servers.

It waits at most 5 seconds for the data to be available on STDIN.

Don't forget the `--report\ option to send to metrology servers.



## Enable the module

Enable the module in the configuration :

    # conf.yml

    modules:
      send:
         enable: yes

## Create a check entry 

    send:
        mytestcheck:
           attribute: mytest
           comment: "This a test comment"
           unit: seconds

        send_mytoken2:
           attribute: mytest2
           comment: "This a second collected entry comment"
           unit: bytes

        (...)

mytestcheck 
    
    the name of the check to use in the CLI call

attribute

    the name of the attribute (prepended with cmt_) sent to metrology servers


comment

    a text string for human explanation in metrology

unit

    the unit of the value being sent
    available : seconds, bytes (for human display only)



## Roadmap

This module may later include options to send a whole file of `attribute:value` as json or yaml.

It may also include targets to raise alerts upon threshold of values processed (much like the folder module).


