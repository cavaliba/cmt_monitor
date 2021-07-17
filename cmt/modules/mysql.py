import os

from MySQLdb import _mysql


# import globals as cmt
import checkitem
from logger import logit, debug, debug2




def check(c):


    # get conf
    host = c.conf.get('host','localhost')
    port = c.conf.get('port','3306')
    user = c.conf.get('user','root')
    password = c.conf.get('password','')
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
        
        vars_slave = {}
        #db.query("show slave status;")
        db.query("select * from information_schema.SYSTEM_VARIABLES;")
        lines=db.store_result().fetch_row(maxrows=0, how=0)
        #db.query("select host,user,password from mysql.user;")
        #lines=db.store_result().fetch_row(maxrows=0, how=2)
        print(lines)

        # for k,v in lines.items():
        #     k=k.decode()
        #     v=v.decode()
        #     vars_slave[k]=v
        #     debug2("mysql-vars_slave : ",c.check,':',k,"=",v)
        #     print(k,v)

        # lines=db.store_result().fetch_row(maxrows=0, how=0)
        # debug2("vars_slave query")
        for (k,v) in lines:
            k=k.decode()
            v=v.decode()
            vars_slave[k]=v
            debug2("mysql-vars_slave : ",c.check,':',k,"=",v)
            print(k,v)


    #db.query("select host,user,password from mysql.user;")
    #lines=db.store_result().fetch_row(maxrows=0, how=0/1/2)
    # for line in lines:
    #     for k,v in line.items():
    #         if k == "version":
    #             print("version=",v)


        # SECONDS_BEHIND_MASTER=$( grep "Seconds_Behind_Master" <<< "$STATUS_LINE" | awk '{ print $2 }')
        # IO_IS_RUNNING=$(grep "Slave_IO_Running:" <<< "$STATUS_LINE" | awk '{ print $2 }')   Yes/No
        # SQL_IS_RUNNING=$(grep "Slave_SQL_Running:" <<< "$STATUS_LINE" | awk '{ print $2 }') Yes/No
        # MASTER_LOG_FILE=$(grep " Master_Log_File" <<< "$STATUS_LINE" | awk '{ print $2 }')
        # RELAY_MASTER_LOG_FILE=$(grep "Relay_Master_Log_File" <<< "$STATUS_LINE" | awk '{ print $2 }')
        
        io_running = vars_slave.get('slave_io_running','No')
        c.add_item(checkitem.CheckItem('slave_io_run',io_running,"Slave_IO_Running"))

        sql_running = vars_slave.get('Slave_SQL_Running','No')
        c.add_item(checkitem.CheckItem('slave_sql_run',sql_running,"Slave_SQL_Running"))
        
        master_log = vars_slave.get('Master_Log_File','n/a')
        c.add_item(checkitem.CheckItem('slave_master_logfile',master_log,"Master_Log_File"))

        relay_log = vars_slave.get('Relay_Master_Log_File','n/a')
        c.add_item(checkitem.CheckItem('slave_relayfile',relay_log,"Relay_Master_Log_File"))

        behind = vars_slave.get('Seconds_Behind_Master', 999999999)
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

    #db.query("select host,user,password from mysql.user;")
    #lines=db.store_result().fetch_row(maxrows=0, how=0/1/2)
    # for line in lines:
    #     for k,v in line.items():
    #         if k == "version":
    #             print("version=",v)

    # not Master / not Slave

    # all OK
    c.add_message("{} - OK - {} ".format(c.check,version))
    return c
