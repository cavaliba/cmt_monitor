# Module cmt ping
# (c) cavaliba.com - 2020/11/22

import subprocess

from cmt_shared import Check, CheckItem


def check_ping(c):

    '''Ping a remote host and return availability'''

    # cmt_ping
    # cmt_ping_status

    #c = Check(module='ping') 
    host = c.conf['host']

    ci = CheckItem('ping',host)
    c.add_item(ci)

    ci = CheckItem('ping_status',"","ok/nok", unit="")

    # TODO : switch to subprocess
    #response = os.system("ping -c 1 -W 2 " + host + "> /dev/null 2>&1")


    proc = subprocess.Popen(
        ["ping", "-c", "1", "-W" "2", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ) # starts the process
    proc.wait() # waits for it to finish (there's a timeout option)
    response = proc.returncode


    if response == 0:
        ci.value = "ok"
        c.add_item(ci)
        c.add_message("{} ok".format(host))

    else:
        ci.value = "nok"
        c.add_item(ci)
        c.alert += 1
        c.add_message("{} not responding".format(host))

    return c