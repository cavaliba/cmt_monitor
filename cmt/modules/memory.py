import psutil

import globals as cmt
from checkitem import CheckItem


def check(c):
    '''Collect memory percent, used, free, available'''


    threshold = c.conf.get('threshold',101)


    # svmem(total=2749374464, available=1501151232, percent=45.4, used=979968000, 
    # free=736043008, active=1145720832, inactive=590102528, buffers=107663360, 
    # cached=925700096, shared=86171648)

    memory = psutil.virtual_memory()

    m1  = CheckItem('memory_percent',memory.percent,"Memory used (percent)", unit = '%')
    c.add_item(m1)

    m2  = CheckItem('memory_used',memory.used,"Memory used (bytes)", unit='bytes')
    h_used = m2.human()
    c.add_item(m2)

    m3  = CheckItem('memory_available',memory.available,"Memory available (bytes)", unit='bytes')
    h_avail = m3.human()
    c.add_item(m3)

    m4  = CheckItem('memory_total',memory.total,"Memory total (bytes)", unit='bytes')
    h_total = m4.human()
    c.add_item(m4)


    # alerts ?
    if float(memory.percent) > float(threshold):
        c.alert += 1
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("memory above threshold : {} % > {} %".format(memory.percent, threshold))
        return c

    # OK
    c.add_message("mem used {} % - used {} - avail {} - total {}".format(memory.percent, h_used, h_avail, h_total) )
    return c
