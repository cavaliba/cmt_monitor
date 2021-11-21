# CMT - MySQL/MariaDB Module
# V1.8.1+
# (c) Cavaliba.com 2021

import time
import subprocess
from MySQLdb import _mysql


import globals as cmt
import checkitem
from logger import logit, debug, debug2


defaults_file = ""


def subprocess_query(q):

    global defaults_file

    #r = subprocess.run(["ls", "-l", "/tmp"], stdout=subprocess.PIPE, timeout=5)
    action = ['mysql' , '--defaults-file=' + defaults_file, '-e',q]
    r = subprocess.run(action, stdout=subprocess.PIPE, timeout=5)
    return r.stdout
    #output = subprocess.check_output(["ls", "/tmp"], shell=True)
    #output = subprocess.check_output(q, shell=True)
    #print(q,output)


def get_derivative(c,vars,name):

    lastrun = cmt.PERSIST.get_key("cmt_last_run", 0)
    delta = int(time.time()) - int(lastrun)
    vnew = float(vars.get(name,0))
    vold =  float(c.persist.get(name,0))
    derivative = (vnew-vold)/delta
    derivative = int( derivative * 100) / 100
    c.persist[name]=vnew
    debug('mysql - derivative : ' + name + ':' + str(derivative))
    return derivative



def check(c):

    global defaults_file

    # get conf
    defaults_file = c.conf.get('defaults_file','/opt/cmt/mysql.cnf')
    # is_master = c.conf.get("is_master", False) is True
    is_slave = c.conf.get("is_slave", False) is True
    max_behind = c.conf.get('max_behind',900)



    try:
        #db=_mysql.connect(host=host,user=user,passwd=password)
        db=_mysql.connect(read_default_file=defaults_file)
    except Exception as e:
        c.alert += 1
        c.severity = cmt.SEVERITY_CRITICAL
        c.add_message("mysql - can't connect with conf {}".format(defaults_file))        
        logit("Error {}".format(e))
        return c

    # -------------------------------------
    # get global CONF
    vars = {}
    db.query("show variables;")

    lines=db.store_result().fetch_row(maxrows=0, how=0)
    for (k,v) in lines:
        k=k.decode()
        v=v.decode()
        vars[k]=v
        debug2("mysql-conf : ",c.check,':',k,"=",v)
        #print(k,v)

    version = vars.get('version','n/a')
    c.add_item(checkitem.CheckItem('mysql_version',version))


    # -------------------------------------
    # get global VARS
    vars = {}
    db.query("show global status;")

    lines=db.store_result().fetch_row(maxrows=0, how=0)
    for (k,v) in lines:
        k=k.decode()
        v=v.decode()
        vars[k]=v
        debug2("mysql-status : ",c.check,':',k,"=",v)
        #print(k,v)


    # Com_select
    # Com_insert
    # Com_update
    # Com_delete
    
    # Connections 175
    # Memory_used 277515936
    # Queries
    # Threads_cached 1
    # Threads_connected 1
    # Threads_created 16
    # Threads_running 8

    thread_c = int(vars.get('Threads_connected',0))
    c.add_item(checkitem.CheckItem('mysql_connection',thread_c))

    thread_r = int(vars.get('Threads_running',0))
    c.add_item(checkitem.CheckItem('mysql_runner',thread_r))

    mem = int(vars.get('Memory_used',0))
    c.add_item(checkitem.CheckItem('mysql_memory',mem,unit='bytes'))

    lastrun = cmt.PERSIST.get_key("cmt_last_run", 0)
    delta = int(time.time()) - int(lastrun)
    
    xconn = 0
    xsel = 0
    xwri = 0
    xqu = 0 

    if delta < 900:

        xsel = get_derivative(c, vars,'Com_select')
        c.add_item(checkitem.CheckItem('mysql_read_rate',xsel,'r/sec'))

        x1 = get_derivative(c, vars,'Com_insert')
        x2 = get_derivative(c, vars,'Com_update')
        x3 = get_derivative(c, vars,'Com_delete')
        xwri = x1 + x2 + x3
        c.add_item(checkitem.CheckItem('mysql_write_rate',xwri ,'w/sec'))

        xqu = get_derivative(c, vars,'Queries')
        c.add_item(checkitem.CheckItem('mysql_query_rate',xqu,'q/sec'))

        xconn = get_derivative(c, vars,'Connections')
        c.add_item(checkitem.CheckItem('mysql_cx_rate',xconn,'connection/sec'))



    # -------------------------------------
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
        for line in lines:
            akv = line.split(':')
            if len(akv) < 2:
                continue
            k=akv[0].rstrip().lstrip()
            v=akv[1].rstrip().lstrip()
            debug2("mysql-slave : ",c.check,':',k,"=",v)
            vars_slave[k]=v               

        
        io_running = vars_slave.get('Slave_IO_Running','No')
        c.add_item(checkitem.CheckItem('mysql_slave_io_run',io_running,"Slave_IO_Running"))

        sql_running = vars_slave.get('Slave_SQL_Running','No')
        c.add_item(checkitem.CheckItem('mysql_slave_sql_run',sql_running,"Slave_SQL_Running"))
        
        master_log = vars_slave.get('Master_Log_File','n/a')
        c.add_item(checkitem.CheckItem('mysql_slave_mpos',master_log,"Master_Log_File"))

        relay_log = vars_slave.get('Relay_Master_Log_File','n/a')
        c.add_item(checkitem.CheckItem('mysql_slave_rpos',relay_log,"Relay_Master_Log_File"))

        behind_str = vars_slave.get('Seconds_Behind_Master', "999999999")
        try:
            behind = int(behind_str)
        except:
            behind = 999999999
        c.add_item(checkitem.CheckItem('mysql_slave_behind',behind,"Seconds_Behind_Master"))


        if io_running != "Yes":
            c.alert += 1
            c.severity = cmt.SEVERITY_CRITICAL
            c.add_message("{} - slave IO not running".format(c.check))
            return c

        if sql_running != "Yes":
            c.alert += 1
            c.severity = cmt.SEVERITY_CRITICAL
            c.add_message("{} - slave SQL not running".format(c.check))
            return c

        if behind > max_behind:
            c.alert += 1
            c.severity = cmt.SEVERITY_CRITICAL
            c.add_message("{} - slave too late behind master {} > {} secs".format(c.check, behind,max_behind))
            return c

        c.add_message("{} - slave {} sec. behind (limit = {}) - cx={} cx/s={} r/s={} w/s={} q/s={} mem={}".format(
                c.check, behind,max_behind,
                thread_c, xconn, xsel, xwri, xqu, mem,
                ))
        return c


    # all OK
    c.add_message("{} - cx={} cx/s={} r/s={} w/s={} q/s={} mem={}".format(
                c.check, thread_c, xconn, xsel, xwri, xqu, mem,
                ))
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

