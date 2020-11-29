
import psutil

#import cmt_globals as cmt
from cmt_shared import Check, CheckItem



def check_cpu(c):

    '''Get CPU percentage. No alert. Send cpu float value.'''

    cpu = psutil.cpu_percent(interval=2)

    # c.persist['cpu'] = cpu

    i  = CheckItem('cpu',cpu,"CPU Percentage", unit='%')   
    c.add_item(i)

    c.add_message("usage : {} %".format(cpu))
    return c
