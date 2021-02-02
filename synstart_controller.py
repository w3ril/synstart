#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ver 1.2 by Petr V. Redkin

import datetime
import socket
import json
from multiprocessing.dummy import Pool as ThreadPool

log_fname = "synstart.log"
daemon_ip = [ '192.168.1.28', '192.168.4.204', '192.168.1.179' ]
daemon_port = 5555
daemon_starting_process = "ls -ltr".split()
daemon_response_timeout = 30
thread_count = len(daemon_ip)
pool = ThreadPool(thread_count) # thread count based on daemon ip count
scheduled_time = datetime.datetime.now() + datetime.timedelta(seconds=5) # start process on daemons in 5 seconds
daemon_command = { "command": "start_process_in_time", "scheduled_start_time": "{}".format(scheduled_time), "daemon_starting_process": daemon_starting_process}
#daemon_command = { "command": "start_process_in_time", "scheduled_start_time": "2021-02-02 16:11:00", "daemon_starting_process": daemon_starting_process}
#daemon_command = { "command": "ntpupdate", "ip": "194.190.168.1"}
#daemon_command = { "command": "queue_status" }


def write_to_file_with_new_line_and_dt(text, fname):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # for log
    with open(fname, 'a') as the_file:
        t = "{} {}".format(dt,text)
        print(t)
        the_file.write(t + '\n')

def send_request(ip):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(daemon_response_timeout)
	write_to_file_with_new_line_and_dt("connecting to daemon_ip {}".format(ip), log_fname)
	connect=sock.connect((ip,daemon_port))
	write_to_file_with_new_line_and_dt("sending daemon_command {} to daemon".format(daemon_command), log_fname)
	j = json.dumps(daemon_command)
	sock.send(j.encode())
	write_to_file_with_new_line_and_dt("waiting ACK from daemon", log_fname)
	data, addr = sock.recvfrom(4096)
	if data == b"OK":
		write_to_file_with_new_line_and_dt("successful communication with daemon", log_fname)
	else:
		write_to_file_with_new_line_and_dt("unsuccessful communication with daemon", log_fname)
		raise Exception("unsuccessful communication with daemon")
	write_to_file_with_new_line_and_dt("closing socket with daemon", log_fname)
	sock.close()


write_to_file_with_new_line_and_dt("syn_start controller started", log_fname)
pool.map(send_request, daemon_ip)