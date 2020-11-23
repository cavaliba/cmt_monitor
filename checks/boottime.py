import time
import psutil

#import cmt_globals as cmt
from cmt_shared import Check, CheckItem

def check_boottime(c):

    #c = Check(module='boottime') 
    boottime = int( time.time() - psutil.boot_time() )
    days = int (boottime / 86400)

    m1 = CheckItem('boottime_seconds',boottime,"Seconds since last reboot", unit='seconds')
    c.add_item(m1)

    m2 = CheckItem('boottime_days',days,'Days since last reboot', unit='days')
    c.add_item(m2)

    # TODO add human format (j/h/m/s)
    c.add_message("Days since last reboot : {} days ({} sec.)".format(days,boottime))
    return c