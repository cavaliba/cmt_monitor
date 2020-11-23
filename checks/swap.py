import psutil

#import cmt_globals as cmt
from cmt_shared import Check, CheckItem

def check_swap(c, conf):

    # sswap(total=2147479552, used=0, free=2147479552, percent=0.0, sin=0, sout=0)
    swap = psutil.swap_memory()

    m1 = CheckItem('swap_percent',swap.percent,"Swap used (percent)", unit = '%')
    c.add_item(m1)

    m2 = CheckItem('swap_used',swap.used,'Swap used (bytes)', unit = 'bytes')
    c.add_item(m2)

    c.add_message("swap used : {} % ".format(swap.percent))
    return c
