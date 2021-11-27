import psutil

import globals as cmt
from checkitem import CheckItem


def check(c):

    # --available option ?
    if cmt.ARGS["available"]:
        print("-" * 25)
        print("Process available :")
        print("-" * 25)
        for p in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                print(p.name())
                print(p.cmdline())
                #print(processName , ' ::: ', processID)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print("-" * 25)
        return c

    # real check

    name = c.check
    psname = c.conf['psname']
    search_arg = c.conf.get('search_arg', None)


    #{'name': 'python3', 'cpu_times': pcputimes(user=0.39, system=0.3, 
    #    children_user=0.0, children_system=0.0), 
    #    'memory_info': pmem(rss=27049984, vms=123904000, shared=13443072, text=3883008, 
    #    lib=0, data=13901824, dirty=0), 'username': 'phil', 'pid': 3125}
    #for proc in psutil.process_iter(['pid', 'name', 'username','cpu_times','memory_info']):
    #     #print(proc.info)

    c.add_item(CheckItem('process_name',psname,"", datapoint=False))

    for proc in psutil.process_iter():

        try:
            # Get process name & pid from process object.
            processName = proc.name()
            # processID = proc.pid
            # print(processName , ' ::: ', processID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        # pinfo = proc.as_dict(attrs=['name','pid','memory_info','cpu_times'])
        if processName  == psname:

            ok = False

            # search args needed (an expected arg is in conf)
            if search_arg:
                try:
                    pargs = proc.cmdline()
                except Exception:
                    pargs = []
                for p in pargs:
                    if p == search_arg:
                        ok = True
                        break
            else:
                # process name is enough, no need to search args
                ok = True

            if ok:
                mem = proc.memory_info().rss
                ci = CheckItem('process_memory',mem,"rss", unit="bytes")
                h_mem = ci.human()
                c.add_item(ci)

                cpu = proc.cpu_times().user
                ci = CheckItem('process_cpu',cpu,"cpu time, user", unit='seconds')
                c.add_item(ci)

                c.add_message("process {} found ({}, {}) - memory rss {} - cpu {} sec.".format(
                        name, psname, search_arg, h_mem, cpu ))
                return c

    c.severity = cmt.SEVERITY_CRITICAL
    c.add_message("process {} missing ({}, {})".format(name, psname, search_arg))

    return c


