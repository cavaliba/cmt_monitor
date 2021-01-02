import time
import psutil

# import globals as cmt
import checkitem


def check(c):

    #c = Check(module='boottime') 
    boottime = int( time.time() - psutil.boot_time() )
    days = int (boottime / 86400)

    m1 = checkitem.CheckItem('boottime_seconds',boottime,"Seconds since last reboot", unit='seconds')
    h_sec = m1.human()
    c.add_item(m1)

    m2 = checkitem.CheckItem('boottime_days',days,'Days since last reboot', unit='days')
    c.add_item(m2)

    c.add_message("boot : {} days since last reboot - {} sec.".format(days,h_sec))
    return c