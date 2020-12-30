import psutil
import socket

import cmt_globals as cmt
from cmt_shared import Check, CheckItem



def socket_tcp_ping(host, port, send='', pattern=''):
    #print("Check Socket - TCP ping test", host, port, send, pattern)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:    
        s.connect((host, port))
        
    except:
        return False
    finally:
        s.close()

    # if len(send)>0:
    #     s.sendall(send)
    # data=""
    # #data = s.recv(1024)
    # print ('Received', repr(data))
    s.close()
    return True


def check_socket(c):

    name = c.check
    socket = c.conf['socket']
    connect = False 
    send = c.conf.get('send', '')
    pattern = c.conf.get('pattern','')
    socparms = socket.split()
    soclocal = "local"
    sochost = ""
    socproto = "tcp"
    socport = ""

    if socparms[0] == "local":
        soclocal = socparms[0]
        socproto = socparms[1]
        socport = int(socparms[2])
        sochost = "localhost"
        connect = c.conf.get('connect',False) == True
    elif socparms[0] == "remote":
        soclocal = socparms[0]
        sochost = socparms[1]
        socproto = socparms[2]
        socport = int(socparms[3])
        connect = c.conf.get('connect',True) == True

    else:
        c.alert += 1
        c.add_message("unknown socket type : {}".format(socparms[0]))       
        return c

# module socket
# -------------
# mysocket:
#   module            : socket
#   socket            : local tcp port | remote host tcp port
#   connect           : yes/no ; default no for local, yes for remote
#   send              : string  ; DEFAULT = no send
#   [pattern]         : "Cavaliba" ; DEFAULT = ""

# reply:

#   cmt_socket_name      : string
#   cmt_socket_type      : local/remote
#   cmt_socket_proto     : tcp/udp
#   cmt_socket_host      : host:port
#   cmt_socket_count     : int (established)
#   cmt_socket_alive     : yes/no  [LISTEN]
#   cmt_socket_ping      : ok/nok

# sconn(fd=150, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='192.168.0.141', port=56094), raddr=addr(ip='52.41.2.143', port=443), status='ESTABLISHED', pid=11077)
# sconn(fd=11, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='192.168.0.141', port=38420), raddr=addr(ip='192.168.0.20', port=445), status='ESTABLISHED', pid=10808)
# sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='192.168.122.1', port=53), raddr=(), status='LISTEN', pid=None)
# sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='127.0.0.1', port=631), raddr=(), status='LISTEN', pid=None)
# sconn(fd=-1, family=<AddressFamily.AF_INET: 2>, type=<SocketKind.SOCK_STREAM: 1>, laddr=addr(ip='127.0.0.53', port=53), raddr=(), status='LISTEN', pid=None)

    c.add_item(CheckItem('socket_name',name,""))
    c.add_item(CheckItem('socket_port',socport,""))

    if soclocal:
        c.add_item(CheckItem('socket_type',"local",""))
    else:
        c.add_item(CheckItem('socket_type',"remote",""))
        c.add_item(CheckItem('socket_host',sochost,""))

    c.add_item(CheckItem('socket_proto',socproto,""))

    #print(connect)
    soccount = 0
    socalive = "no"

    # UDP
    if socproto == "udp":
        c.add_message("UDP socket not implemented for {}".format(name))
        c.alert += 1
        return c


    # TCP local
    if soclocal == "local"  and socproto == "tcp":
        items = psutil.net_connections(kind='tcp4')
        for item in items:
            p = int(item.laddr.port)
            if p == socport:
                if item.status == 'LISTEN':
                    socalive = "yes"
                elif item.status == 'ESTABLISHED':
                    soccount += 1
        c.add_item(CheckItem('socket_alive',socalive,""))
        c.add_item(CheckItem('socket_count',soccount,""))

        if socalive == "no":
            c.add_message("socket {} {} {} {}/{} not alive (no LISTEN)".format(soclocal, name, sochost, socproto,socport))
            c.alert += 1
            return c

        # socket_tcp_ping
        if connect:
            r = socket_tcp_ping(sochost,socport)
            if not r:
                c.add_message("socket {} {} {} {}/{} no response / bad response".format(soclocal, name, sochost, socproto,socport))
                c.alert += 1
                return c


    # TCP remote
    if soclocal =="remote"  and socproto == "tcp":

        socalive = "n/a"

        items = psutil.net_connections(kind='tcp4')
        for item in items:
            p = int(item.laddr.port)
            if p == socport:
                if item.status == 'ESTABLISHED':
                    soccount += 1
                    socalive = "yes"
        c.add_item(CheckItem('socket_count',soccount,""))
        
        # TODO
        # socket_tcp_ping
        if connect:
            r = socket_tcp_ping(sochost,socport)
            if not r:
                socalive = "no"
                c.add_item(CheckItem('socket_alive',socalive,""))
                c.add_message("socket {} {} {} {}/{} no response / bad response".format(soclocal, name, sochost, socproto,socport))
                c.alert += 1
                return c
            else:
                socalive = "yes"
                c.add_item(CheckItem('socket_alive',socalive,""))
        else:
            # use value from counting ESTABLSHED
            c.add_item(CheckItem('socket_alive',socalive,""))

    c.add_message("socket {} {} {} {}/{} - alive: {} - count: {}".format(soclocal, name, sochost, socproto,socport, socalive, soccount))
    return c


