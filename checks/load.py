
import os

#import cmt_globals as cmt
from cmt_shared import Check, CheckItem


def check_load(c):
    

    # (1.17, 0.86, 0.52)
    load = os.getloadavg()

    l1  = CheckItem('load1',load[0])
    l1.description ='CPU Load Average, one minute'
    c.add_item(l1)

    l5  = CheckItem('load5',load[1])
    l5.description='CPU Load Average, 5 minutes'
    c.add_item(l5)

    l15 = CheckItem('load15',load[2])
    l15.description='CPU Load Average, 15 minutes'
    c.add_item(l15)
    
    c.add_message("1/5/15 min : {}  {}  {}".format(load[0], load[1], load[2]))
    return c
