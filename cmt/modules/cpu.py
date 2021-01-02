
import psutil

# import globals as cmt
import checkitem

def check(c):

    '''Get CPU percentage. No alert. Send cpu float value.'''

    cpu = psutil.cpu_percent(interval=2)

    # c.persist['cpu'] = cpu

    i  = checkitem.CheckItem('cpu',cpu,"CPU Percentage", unit='%')   
    c.add_item(i)

    c.add_message("cpu usage : {} %".format(cpu))
    return c
