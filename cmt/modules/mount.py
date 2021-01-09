import psutil

import globals as cmt
from checkitem import CheckItem


def check(c):
    '''Checks mount points
       OUTPUT
         - cmt_mount
    '''

    partitions=psutil.disk_partitions(all=True)

    if cmt.ARGS["available"]:
        print("-" * 25)
        print("Available mountpoints :")
        print("-" * 25)
        for p in partitions:
            print(p)
        print("-" * 25)
        return c


    # sdiskpart(device='/dev/sda1', mountpoint='/', fstype='ext4', 
    #               opts='rw,relatime,errors=remount-ro,data=ordered')

    path = c.conf['path']

    ci = CheckItem('mount',path)
    c.add_item(ci)

    for part in partitions:
        if part.mountpoint == path:
            c.add_message("mount {} found".format(path))
            return c

    c.alert += 1
    c.add_message("mount {} not found".format(path))

    return c
