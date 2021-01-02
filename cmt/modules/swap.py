import psutil

# import globals as cmt
from checkitem import CheckItem

def check(c):

    # sswap(total=2147479552, used=0, free=2147479552, percent=0.0, sin=0, sout=0)
    swap = psutil.swap_memory()

    m1 = CheckItem('swap_percent',swap.percent,"Swap used (percent)", unit = '%')
    c.add_item(m1)

    m2 = CheckItem('swap_used',swap.used,'Swap used (bytes)', unit = 'bytes')
    h_used = m2.human()
    c.add_item(m2)

    m3 = CheckItem('swap_total',swap.total,'Swap total (bytes)', unit = 'bytes')
    h_total = m3.human()
    c.add_item(m3)


    c.add_message("swap used: {} % /  {} - total {}".format(swap.percent, h_used, h_total))
    return c
