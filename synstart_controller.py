#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ver 1.3 by Petr V. Redkin

import datetime
import socket
import json
from multiprocessing.dummy import Pool as ThreadPool

log_fname = "synstart.log"
daemon_ip = [ '192.168.1.28', '192.168.4.204', '192.168.1.179' ]
daemon_port = 5555
daemon_starting_process = "ls -ltr".split()
thread_count = len(daemon_ip)
pool = ThreadPool(thread_count) # thread count based on daemon ip count
scheduled_time = datetime.datetime.now() + datetime.timedelta(seconds=5) # start process on daemons in 5 seconds
daemon_command = { "command": "start_process_in_time", "scheduled_start_time": "{}".format(scheduled_time), "daemon_starting_process": daemon_starting_process}
#daemon_command = { "command": "start_process_in_time", "scheduled_start_time": "2021-02-02 16:11:00", "daemon_starting_process": daemon_starting_process}
#daemon_command = { "command": "ntpupdate", "ip": "194.190.168.1"}
#daemon_command = { "command": "queue_status" }


def send_request(ip):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# use short TCP keepalives as execution timeout
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
	#sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
	print("connecting to daemon_ip {}".format(ip))
	connect=sock.connect((ip,daemon_port))
	print("sending daemon_command {} to daemon".format(daemon_command))
	j = json.dumps(daemon_command)
	sock.send(j.encode())
	print("waiting ACK from daemon")
	data = sock.recv(4096)
	if data == b"OK":
		print("successful communication with daemon")
	else:
		print("unsuccessful communication with daemon")
		raise Exception("unsuccessful communication with daemon")
	print("closing socket with daemon")
	sock.close()


print("syn_start controller started")
pool.map(send_request, daemon_ip)