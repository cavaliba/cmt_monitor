
import psutil

#import cmt_globals as cmt
from cmt_shared import Check, CheckItem



def check_cpu(c):

    '''Get CPU percentage. No alert. Send cpu float value.'''

    cpu = psutil.cpu_percent(interval=2)

    i  = CheckItem('cpu',cpu,"CPU Percentage", unit='%')   
    c.add_item(i)

    c.add_message("CPU = {} %".format(cpu))
    return c
