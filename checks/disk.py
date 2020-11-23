import psutil

import cmt_globals as cmt
from cmt_shared import Check, CheckItem

# df -k
def check_disk(c,conf):

    #c = Check(module='disk') 
    path = conf['path']
    alert_threshold = int(conf['alert'])

    # sdiskusage(total=21378641920, used=4809781248, free=15482871808, percent=22.5)
    disk=psutil.disk_usage(path)

    ci = CheckItem('disk',path,"Path")
    c.add_item(ci)

    ci = CheckItem('disk_total',disk[0],"Total (Bytes)", unit='bytes')
    c.add_item(ci)

    ci = CheckItem('disk_free',disk[2],"Free (Bytes)", unit='bytes')
    c.add_item(ci)

    ci = CheckItem('disk_percent',disk[3],"Used (percent)", unit='%')
    if disk[3] > alert_threshold:
        c.alert += 1
        c.add_message("Disk {} - critical capacity ({} %)".format(path,disk[3]))

    else:
        c.add_message("Disk {} - bytes free {}/{}  -  used percent {} %".format(path, disk[2], disk[0], disk[3]))
    
    c.add_item(ci)

    return c
