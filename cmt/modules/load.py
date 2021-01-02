import os

# import globals as cmt
import checkitem


def check(c):

    # (1.17, 0.86, 0.52)
    load = os.getloadavg()

    l1  = checkitem.CheckItem('load1',load[0])
    l1.description ='CPU Load Average, one minute'
    c.add_item(l1)

    l5  = checkitem.CheckItem('load5',load[1])
    l5.description='CPU Load Average, 5 minutes'
    c.add_item(l5)

    l15 = checkitem.CheckItem('load15',load[2])
    l15.description='CPU Load Average, 15 minutes'
    c.add_item(l15)

    c.add_message("load 1/5/15 min : {}  {}  {}".format(load[0], load[1], load[2]))
    return c
