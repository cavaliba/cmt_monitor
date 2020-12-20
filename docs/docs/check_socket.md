---
title: check_socket
---

# Check: Socket

**Socket** checks a local or remote TCP socket with the following criterions :

- for local, check if LISTEN socket is present
- for local and remote, count ESTABLISHED
- for remote, or if connect option is given, try to connect


This check can be used to monitor remote process network availability, and count how many  sockets are currently in use for some protocols.


## Enable the module

Enable the module in the configuration :

    # conf.yml

	modules:
  	  socket:
  	     enable: yes

## Additional parameters

	socket:
	    mysocket:
	       socket       : local tcp port | remote host tcp port
	       connect      : yes/no ; default no for local, yes for remote

Example

	socket:
		redis:
		    socket: local tcp 6379
		    connect: yes

		google:
		    socket: remote www.google.com tcp 443
		    connect: yes


## Alerts

This check sends an alert if a local socket is not in LISTEN state, or if a socket refuse connection.


## Output to ElasticSearch

This module sends one message for each socket, with the following fields:

	cmt_socket_name      : string
	cmt_socket_type      : local/remote
	cmt_socket_proto     : tcp/udp
	cmt_socket_host      : host:port
	cmt_socket_count     : int (established)
	cmt_socket_alive     : yes/no  [LISTEN]
	cmt_socket_ping      : ok/nok


## CLI usage and output

	$ ./cmt.py socket 

	Check socket 
	cmt_socket_name          redis
	cmt_socket_port          6379
	cmt_socket_type          local
	cmt_socket_proto         tcp
	cmt_socket_alive         yes
	cmt_socket_count         0
	OK                       local redis localhost tcp/6379 - alive: yes - count: 0

	Check socket 
	cmt_socket_name          google
	cmt_socket_port          443
	cmt_socket_type          local
	cmt_socket_proto         tcp
	cmt_socket_count         0
	cmt_socket_alive         yes
	OK                       remote google www.google.com tcp/443 - alive: yes - count: 0








