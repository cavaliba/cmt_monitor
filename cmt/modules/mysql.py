import os

import subprocess
from MySQLdb import _mysql


# import globals as cmt
import checkitem
from logger import logit, debug, debug2


defaults_file = ""
mysql_cmd = "mysql"



def subprocess_query(q):

    global mysql_cmd
    global defaults_file

    #r = subprocess.run(["ls", "-l", "/tmp"], stdout=subprocess.PIPE, timeout=5)
    action = [mysql_cmd , '--defaults-file='+defaults_file, '-e',q]
    debug(action)
    r = subprocess.run(action, stdout=subprocess.PIPE, timeout=5)
    return r.stdout
    #output = subprocess.check_output(["ls", "/tmp"], shell=True)
    #output = subprocess.check_output(q, shell=True)
    #print(q,output)


def check(c):

    global mysql_cmd
    global defaults_file

    # get conf
    host = c.conf.get('host','localhost')
    port = c.conf.get('port','3306')
    user = c.conf.get('user','root')
    password = c.conf.get('password','')
    defaults_file = c.conf.get('defaults_file','/opt/cmt/mysql.cnf')
    is_master = c.conf.get("is_master", False) is True
    is_slave = c.conf.get("is_slave", False) is True
    max_behind = c.conf.get('max_behind',900)

    #is_master = c.conf.get("is_master", False) is True



    try:
        db=_mysql.connect(host=host,user=user,passwd=password)
    except Exception as e:
        c.alert += 1
        c.add_message("mysql - can't connect to {} with user {}".format(host,user))        
        logit("Error {}".format(e))
        return c

    # global variables
    vars = {}
    db.query("show variables;")

    lines=db.store_result().fetch_row(maxrows=0, how=0)
    for (k,v) in lines:
        k=k.decode()
        v=v.decode()
        vars[k]=v
        debug2("mysql-vars : ",c.check,':',k,"=",v)
        #print(k,v)

    #print(vars["version"])
    version = vars.get('version','n/a')
    c.add_item(checkitem.CheckItem('mysql_version',version))


    # SLAVE INFO
    if is_slave:

        debug2("vars_slave query")
        
        #q = 'select 1;'
        #q = 'select host,user from mysql.user;'
        q = 'show slave status\G'
        r = subprocess_query(q).decode()

        # cut on newlines, remove trailing spaces, split on first space, get k,v
        vars_slave = {}
        lines = r.split('\n')
        for l in lines:
            akv = l.split(':')
            if len(akv) < 2:
                continue
            k=akv[0].rstrip().lstrip()
            v=akv[1].rstrip().lstrip()
            debug2("mysql-vars_slave : ",c.check,':',k,"=",v)
            vars_slave[k]=v               

        
        io_running = vars_slave.get('Slave_IO_Running','No')
        c.add_item(checkitem.CheckItem('slave_io_run',io_running,"Slave_IO_Running"))

        sql_running = vars_slave.get('Slave_SQL_Running','No')
        c.add_item(checkitem.CheckItem('slave_sql_run',sql_running,"Slave_SQL_Running"))
        
        master_log = vars_slave.get('Master_Log_File','n/a')
        c.add_item(checkitem.CheckItem('slave_master_logfile',master_log,"Master_Log_File"))

        relay_log = vars_slave.get('Relay_Master_Log_File','n/a')
        c.add_item(checkitem.CheckItem('slave_relayfile',relay_log,"Relay_Master_Log_File"))

        behind_str = vars_slave.get('Seconds_Behind_Master', "999999999")
        try:
            behind = int(behind_str)
        except:
            behind = 999999999
        c.add_item(checkitem.CheckItem('slave_behind',behind,"Seconds_Behind_Master"))


        if io_running != "Yes":
            c.alert += 1
            c.add_message("{} - slave IO not running".format(c.check))
            return c

        if sql_running != "Yes":
            c.alert += 1
            c.add_message("{} - slave SQL not running".format(c.check))
            return c

        if behind > max_behind:
            c.alert += 1
            c.add_message("{} - slave too late behind master {} > {} secs".format(c.check, behind,max_behind))
            return c

        c.add_message("{} - slave OK - {} secs behind master (limit = {})".format(c.check, behind,max_behind))
        return c


    if is_master:
        c.add_message("{} - master OK - {}".format(c.check,version))
        return c

    # not Master / not Slave

    # all OK
    c.add_message("{} - OK - {} ".format(c.check,version))
    return c


# code / template 

    #db.query("select host,user,password from mysql.user;")
    #lines=db.store_result().fetch_row(maxrows=0, how=0/1/2)
    # for line in lines:
    #     for k,v in line.items():
    #         if k == "version":
    #             print("version=",v)

    # for k,v in lines.items():
    #     k=k.decode()
    #     v=v.decode()
    #     vars_slave[k]=v
    #     debug2("mysql-vars_slave : ",c.check,':',k,"=",v)
    #     print(k,v)

    # lines=db.store_result().fetch_row(maxrows=0, how=0)
    # debug2("vars_slave query")
    # for (k,v) in lines:
    #     k=k.decode()
    #     v=v.decode()
    #     vars_slave[k]=v
    #     debug2("mysql-vars_slave : ",c.check,':',k,"=",v)
    #     print(k,v)


    #db.query("select host,user,password from mysql.user;")
    #lines=db.store_result().fetch_row(maxrows=0, how=0/1/2)
    # for line in lines:
    #     for k,v in line.items():
    #         if k == "version":
    #             print("version=",v)

