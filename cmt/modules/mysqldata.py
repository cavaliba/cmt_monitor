# CMT - mysqldata Module
# V2.0
# (c) Cavaliba.com 2021

import time
import subprocess
from MySQLdb import _mysql


import globals as cmt
import checkitem
from logger import logit, debug, debug2


defaults_file = ""


def check(c):

    global defaults_file

    # mysql server endpoint and credentials
    defaults_file = c.conf.get('defaults_file','/opt/cmt/mysql.cnf')

    query = c.conf.get('query','')
    columns = c.conf.get('columns',{})
    maxlines = c.conf.get('maxlines',200)

    # -------------------------------------

    try:
        #db=_mysql.connect(host=host,user=user,passwd=password)
        db=_mysql.connect(read_default_file=defaults_file)
    except Exception as e:
        c.alert += 1
        c.add_message("mysql - can't connect with conf {}".format(defaults_file))        
        logit("Error {}".format(e))
        return c

    # -------------------------------------
    
    db.query(query)
    lines=db.store_result().fetch_row(maxrows=0, how=1)
    #  ( {'id': b'1', 'user': b'joe',  'age': b'33'}, 
    #    {'id': b'2', 'user': b'igor', 'age': b'23'}, 
    #    {'id': b'3', 'user': b'phil', 'age': b'42'}   )

    # print(lines)
    count = 0
    for line in lines:
        vars = {}
        count = count + 1
        if count >= maxlines:
            break

        for k,v in line.items():
            try:
                v = v.decode()
            except:
                pass 
            try:
                k2 = columns[k]
            except:
                k2 = k
            print(k2,v)
            vars[k2]=v
        c.multievent.append(vars)

    # create global event
    c.add_item(checkitem.CheckItem('mysqldata_count',count))

    c.add_message("{} - {} lines collected".format( c.check, count ))
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

