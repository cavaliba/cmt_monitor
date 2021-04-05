
import psutil

# import globals as cmt
import checkitem

def check(c):

    '''Get CPU percentage. No alert. Send cpu float value.'''

    threshold = c.conf.get('threshold',101)


    cpu = psutil.cpu_percent(interval=2)

    # c.persist['cpu'] = cpu

    i  = checkitem.CheckItem('cpu',cpu,"CPU Percentage", unit='%')   
    c.add_item(i)

    # alerts ?
    if float(cpu) > float(threshold):
        c.alert += 1
        c.add_message("cpu above threshold : {} % > {} %".format(cpu, threshold))
        return c

    # OK
    c.add_message("cpu usage : {} %".format(cpu))
    return c
