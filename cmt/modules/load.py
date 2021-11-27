import os

import globals as cmt
import checkitem


def is_above_threshold(load, threshold):
    if float(load) > float(threshold):
        return True
    return False


def check(c):


    threshold1 = c.conf.get('threshold1',999999)
    threshold5 = c.conf.get('threshold5',999999)
    threshold15 = c.conf.get('threshold15',999999)


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

    # alerts ?
    if is_above_threshold(load[0], threshold1):
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("load1 above threshold : {} > {} ".format(load[0], threshold1))
        return c
    if is_above_threshold(load[1], threshold5):
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("load5 above threshold : {} > {} ".format(load[1], threshold5))
        return c
    if is_above_threshold(load[2], threshold15):
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("load15 above threshold : {} > {} ".format(load[2], threshold15))
        return c

    # all OK
    c.add_message("load 1/5/15 min : {}  {}  {}".format(load[0], load[1], load[2]))
    return c
