import os

import globals as cmt
import checkitem

cpu_count = 1


def is_above_threshold(load, threshold):

    if float(load) > float ( cpu_count * threshold ):
        return True

    return False

def check(c):

    global cpu_count

    threshold1 = c.conf.get('threshold1',5)
    threshold5 = c.conf.get('threshold5',2)
    threshold15 = c.conf.get('threshold15',1)


    cpu_count = os.cpu_count()
    l = checkitem.CheckItem('load_cpu',cpu_count)
    l.description='Available CPUs'
    c.add_item(l)

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
    if is_above_threshold(load[2], threshold15):
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("load-15/cpu is above threshold : {} > {} ({} cpus)".format(load[2], threshold15 * cpu_count, cpu_count))
        return c

    if is_above_threshold(load[1], threshold5):
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("load-5/cpu is above threshold : {} > {} ({} cpus)".format(load[1], threshold5 * cpu_count, cpu_count))
        return c

    if is_above_threshold(load[0], threshold1):
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("load-1/cpu is above threshold : {} > {} ({} cpus)".format(load[0], threshold1 * cpu_count, cpu_count))
        return c

    # all OK
    c.add_message("load 1/5/15 min : {}  {}  {} ({} cpus)".format(load[0], load[1], load[2], cpu_count))
    return c
