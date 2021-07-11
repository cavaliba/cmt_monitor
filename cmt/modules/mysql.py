import os

# import globals as cmt
import checkitem
from MySQLdb import _mysql


def check(c):


    # get conf
    host = c.conf.get('host','localhost')
    user = c.conf.get('user','root')
    password = c.conf.get('password','')
    is_slave = c.conf.get("is_slave", False) is True
    max_behind = c.conf.get('max_behind',900)

    #is_master = c.conf.get("is_master", False) is True


    db=_mysql.connect(host=host,user=user,passwd=password)

    vars = {}
    db.query("show variables;")

    lines=db.store_result().fetch_row(maxrows=0, how=0)
    for (k,v) in lines:
        k=k.decode()
        v=v.decode()
        vars[k]=v
        #print(k,v)


    #print(vars["version"])

    version = vars.get('version','n/a')

    c.add_item(checkitem.CheckItem('mysql_version',version))


    # SLAVE INFO
    if is_slave:
    
        # SECONDS_BEHIND_MASTER=$( grep "Seconds_Behind_Master" <<< "$STATUS_LINE" | awk '{ print $2 }')
        # IO_IS_RUNNING=$(grep "Slave_IO_Running:" <<< "$STATUS_LINE" | awk '{ print $2 }')   Yes/No
        # SQL_IS_RUNNING=$(grep "Slave_SQL_Running:" <<< "$STATUS_LINE" | awk '{ print $2 }') Yes/No
        # MASTER_LOG_FILE=$(grep " Master_Log_File" <<< "$STATUS_LINE" | awk '{ print $2 }')
        # RELAY_MASTER_LOG_FILE=$(grep "Relay_Master_Log_File" <<< "$STATUS_LINE" | awk '{ print $2 }')
        
        io_running = vars.get('Slave_IO_Running','No')
        c.add_item(checkitem.CheckItem('slave_io_run',io_running,"Slave_IO_Running"))

        sql_running = vars.get('Slave_SQL_Running','No')
        c.add_item(checkitem.CheckItem('slave_sql_run',sql_running,"Slave_SQL_Running"))
        
        master_log = vars.get('Master_Log_File','n/a')
        c.add_item(checkitem.CheckItem('slave_master_logfile',master_log,"Master_Log_File"))

        relay_log = vars.get('Relay_Master_Log_File','n/a')
        c.add_item(checkitem.CheckItem('slave_relayfile',relay_log,"Relay_Master_Log_File"))

        behind = vars.get('Seconds_Behind_Master', 999999999)
        c.add_item(checkitem.CheckItem('slave_behind',behind,"Seconds_Behind_Master"))


        if io_running != "Yes":
            c.alert += 1
            c.add_message("mysql - slave IO not running")
            return c

        if sql_running != "Yes":
            c.alert += 1
            c.add_message("mysql - slave SQL not running")
            return c

        if behind > max_behind:
            c.alert += 1
            c.add_message("mysql - slave too late behind master {} > {} secs".format(behind,max_behind))
            return c

        c.add_message("mysql - slave OK - {} secs behind master (limit = {}".format(behind,max_behind))
        return c

    #db.query("select host,user,password from mysql.user;")
    #lines=db.store_result().fetch_row(maxrows=0, how=0/1/2)
    # for line in lines:
    #     for k,v in line.items():
    #         if k == "version":
    #             print("version=",v)


    # all OK
    c.add_message("mysql - OK - {} ".format(version))
    return c
