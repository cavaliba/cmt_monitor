# Module cmt ping
# (c) cavaliba.com - 2020/11/22

import subprocess

# import globals as cmt
from checkitem import CheckItem


def check(c):
    '''Ping a remote host and return availability
       Output:
          - cmt_ping
    '''

    host = c.conf['host']

    ci = CheckItem('ping', host)
    c.add_item(ci)

    # response = os.system("ping -c 1 -W 2 " + host + "> /dev/null 2>&1")
    proc = subprocess.Popen(
        ["ping", "-c", "1", "-W" "2", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )    # starts the process
    proc.wait()    # waits for it to finish (there's a timeout option)
    response = proc.returncode

    if response == 0:
        c.add_message("ping {} ok".format(host))
    else:
        c.alert += 1
        c.add_message("ping {} not responding".format(host))

    return c
