#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ver 1.1 by Petr V. Redkin

import datetime
import socket
from multiprocessing.dummy import Pool as ThreadPool

log_fname = "synstart.log"
daemon_ip = [ '192.168.1.28', '192.168.1.29', '192.168.4.204' ]
daemon_port = 5555
thread_count = len(daemon_ip)
pool = ThreadPool(thread_count) # thread count based on daemon ip count
command = b"start_process_in_time 2021-02-02 11:18:00"
#command = b"ntpupdate 194.190.168.1"
#command = b"queue_status"

def write_to_file_with_new_line_and_dt(text, fname):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # for log
    with open(fname, 'a') as the_file:
        t = "{} {}".format(dt,text)
        print(t)
        the_file.write(t + '\n')

def send_request(ip):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	write_to_file_with_new_line_and_dt("connecting to daemon_ip {}".format(ip), log_fname)
	connect=sock.connect((ip,daemon_port))
	write_to_file_with_new_line_and_dt("sending command {} to daemon".format(command), log_fname)
	sock.send(command)
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