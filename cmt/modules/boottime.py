import time
import psutil

import globals as cmt
import checkitem


# yes/no check   (above threshold)

def check(c):

    threshold = c.conf.get('threshold',99999)


    #c = Check(module='boottime') 
    boottime = int( time.time() - psutil.boot_time() )
    days = int (boottime / 86400)

    m1 = checkitem.CheckItem('boottime_seconds',boottime,"Seconds since last reboot", unit='seconds')
    h_sec = m1.human()
    c.add_item(m1)

    m2 = checkitem.CheckItem('boottime_days',days,'Days since last reboot', unit='days')
    c.add_item(m2)

    # alerts ?
    if float(days) > float(threshold):
        c.alert += 1
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("boottime above threshold : {} days > {} days".format(days, threshold))
        return c

    # OK
    c.add_message("boot : {} days since last reboot - {} sec.".format(days,h_sec))
    return c