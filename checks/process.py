import psutil

import cmt_globals as cmt
from cmt_shared import Check, CheckItem


def check_process(c):

    # --available option ?
    if cmt.ARGS["available"]:
        print("-" * 25)
        print("Process available :")
        print("-" * 25)
        for p in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                print(p.name())
                #print(processName , ' ::: ', processID)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print("-" * 25)
        return c

    # real check

    name = c.name
    psname = c.conf['psname']

    #{'name': 'python3', 'cpu_times': pcputimes(user=0.39, system=0.3, 
    #    children_user=0.0, children_system=0.0), 
    #    'memory_info': pmem(rss=27049984, vms=123904000, shared=13443072, text=3883008, 
    #    lib=0, data=13901824, dirty=0), 'username': 'phil', 'pid': 3125}
    #for proc in psutil.process_iter(['pid', 'name', 'username','cpu_times','memory_info']):
    #     #print(proc.info)

    ci = CheckItem('process_name',name,"")
    c.add_item(ci)

    
    for proc in psutil.process_iter():

        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            #print(processName , ' ::: ', processID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        # pinfo = proc.as_dict(attrs=['name','pid','memory_info','cpu_times'])
        if processName  == psname:


            mem = proc.memory_info().rss
            ci = CheckItem('process_memory',mem,"rss", unit="bytes")
            h_mem = ci.human()
            c.add_item(ci)
            
            cpu = proc.cpu_times().user
            ci = CheckItem('process_cpu',cpu,"cpu time, user", unit='seconds')
            c.add_item(ci)

            c.add_message("process {} found ({}) - memory rss {} - cpu {} sec.".format(name, psname, h_mem, cpu ))
            return c

    c.alert += 1
    c.add_message("process {} missing ({})".format(name, psname))

    return c


