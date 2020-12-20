import psutil

import cmt_globals as cmt
from cmt_shared import Check, CheckItem

# df -k
def check_disk(c):

    #c = Check(module='disk') 
    path = c.conf['path']
    alert_threshold = int(c.conf['alert'])

    # sdiskusage(total=21378641920, used=4809781248, free=15482871808, percent=22.5)
    disk=psutil.disk_usage(path)

    ci = CheckItem('disk',path,"Path")
    c.add_item(ci)

    ci = CheckItem('disk_total',disk[0],"Total (Bytes)", unit='bytes')
    h_total = ci.human()
    c.add_item(ci)

    ci = CheckItem('disk_used',disk[1],"Used (Bytes)", unit='bytes')
    h_used = ci.human()
    c.add_item(ci)

    ci = CheckItem('disk_free',disk[2],"Free (Bytes)", unit='bytes')
    h_free = ci.human()
    c.add_item(ci)

    ci = CheckItem('disk_percent',disk[3],"Used (percent)", unit='%')
    if disk[3] > alert_threshold:
        c.alert += 1
        c.add_message("disk {} - critical capacity ({} %)".format(path,disk[3]))

    else:
        c.add_message("disk {} - used: {} % - used: {} - free: {} - total: {} ".format(path, disk[3],h_used, h_free,h_total))
    
    c.add_item(ci)

    return c
