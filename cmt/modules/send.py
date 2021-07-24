# cmt  send.py

# Use case
# - echo "data" | cmt send --token keyid

import sys
import select

# import globals as cmt
from checkitem import CheckItem

def get_value():
    # not a problem for single check run accross all cmt
    timeout = 5
    if sys.stdin in select.select([sys.stdin], [], [], timeout)[0]:
        for line in sys.stdin:
            return line.rstrip()
    return ""


def check(c):

    '''
    Get data from CLI / pipe and send ; single check mode only 
    '''

    # must no run in cron mode, or multi module/checks mode (because read on stdin)
    if not (c.opt["single_module_run"] and c.opt["specific_checkname_run"]):
        c.result = "skip"
        return c

    #name = c.check
    attribute = c.conf['attribute']
    unit = c.conf.get("unit","")
    comment = c.conf.get("comment","")

    #quote = c.conf.get("quote", False) is True
    # source = c.conf['source']
    # targets = []
    # if 'target' in c.conf:
    #     targets = c.conf['target']
    
    #c.add_item(CheckItem('name',value))

    #ci = CheckItem('folder_size',s_size,"Total Size (bytes)", unit="bytes")
    #h_size = ci.human()
    #c.add_item(ci)

    value = get_value()


    c.add_item(CheckItem(attribute,value,comment, unit))    

    c.add_message("{} = {} - (unit = {} - {})".format(attribute, value, unit, comment))
        
    return c
