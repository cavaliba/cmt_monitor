# cmt  sendfile.py


import sys
import json 

# import globals as cmt
from checkitem import CheckItem
from logger import logit, debug, debug2



def check(c):

    '''
    Sends a [json] file with key/values as single/multiple events (array) to metrology servers
    '''

    jsonfile = c.conf.get('jsonfile',"")
    data = []

    #  [ {k:v, k:v ...} , {k:v, k:v, ...}, {}, ...]
    try:
        with open(jsonfile, "r") as fi:
            data = fi.read()
    except Exception as e:
        debug("ERROR - Persist() : couldn't read file {} - {}".format(jsonfile, e))

    try:
        myarray = json.loads(data)
    except Exception as e:
        debug("ERROR - Persist() : couldn't decode data - {}".format(e))

    # TODO : check if file changed / option change_only
    # TODO : keymap to rewrite key names

    c.multievent = myarray
    count = len(myarray)

    # count = 0
    # for event in myarray:
    #     count = count + 1
    #     print ("event {}".format(count))
    #     dico = {}
    #     for k,v in event.items():
    #         print(k,v)
    #         dico[k]=v
    #         ci = CheckItem(k,v)
    #         c.multievent[]

    c.add_item(CheckItem("sendfile_name",jsonfile))
    c.add_item(CheckItem("sendfile_lines",count))
    c.add_message("{} - {} lines/events".format(jsonfile, count))

    #print (c.multievent)
        
    return c
