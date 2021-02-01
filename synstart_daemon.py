#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ver 1.0 by Petr V. Redkin

import datetime
import time
import socket
import subprocess

log_fname = "synstart.log"
daemon_ip = '0.0.0.0'
daemon_port = 5555
controller_ip = ['192.168.1.28', '192.168.1.29', '192.168.1.179']
sleep_time = 1/1000 # 1 msec (1/1000 of second) default; change for more precision but higher CPU load
starting_process_cmd = "date"

def write_to_file_with_new_line_and_dt(text, fname):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # for log
    with open(fname, 'a') as the_file:
        t = "{} {}".format(dt,text)
        print(t)
        the_file.write(t + '\n')

def convert_str_time_to_int(str_time):
	return int(str_time.replace(" ", "").replace(":", "").replace("-", "").replace("-", "").replace(".", ""))

def start_process_in_time(stime):
	write_to_file_with_new_line_and_dt("starting start_process_in_time: stime {}".format(stime), log_fname)
	ln = len(stime)
	stime_to_compare = convert_str_time_to_int(stime)
	while True:
		actual_time = str(datetime.datetime.now())
		actual_time_to_compare = convert_str_time_to_int(actual_time[0:ln])
		if actual_time_to_compare >= stime_to_compare:
			res = subprocess.run(starting_process_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
			write_to_file_with_new_line_and_dt("finished start_process_in_time: stime {}, stime_to_compare {}, stime length {}, actual stime {}, actual actual_time_to_compare {} result {}".format(stime, stime_to_compare, ln, actual_time, actual_time_to_compare, res), log_fname)
			return
		time.sleep(sleep_time)

def check_start_time(stime):
	write_to_file_with_new_line_and_dt("starting check_start_time: stime {}".format(stime), log_fname)
	ln = len(stime)
	stime_to_compare = convert_str_time_to_int(stime)
	actual_time = str(datetime.datetime.now())
	actual_time_to_compare = convert_str_time_to_int(actual_time[0:ln])
	if actual_time_to_compare >= stime_to_compare:
		res = False
	else:
		res = True
	write_to_file_with_new_line_and_dt("finished check_start_time: stime {}, stime_to_compare {}, stime length {}, actual stime {}, actual actual_time_to_compare {} result {}".format(stime, stime_to_compare, ln, actual_time, actual_time_to_compare, res), log_fname)
	return res

def ntpupdate(ntp_server):
	write_to_file_with_new_line_and_dt("starting ntpupdate: ntp_server {}".format(ntp_server), log_fname)
	cmd = "ntpdate {}".format(ntp_server).split(" ")
	res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
	write_to_file_with_new_line_and_dt("finished ntpupdate: ntp_server {}; result {}".format(ntp_server, res), log_fname)
	if res.returncode == 0:
		return True
	else:
		return False



write_to_file_with_new_line_and_dt("syn_start daemon started, expected time format for start_process_in_time function is \"{}\"".format(str(datetime.datetime.now())), log_fname)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind ((daemon_ip,daemon_port))
while True:
	data, addr = sock.recvfrom(4096)
	# 1 - basic auth
	if addr[0] in controller_ip:
		write_to_file_with_new_line_and_dt("udp data received from trusted controller ip/port: {}; data: {}".format(addr, data), log_fname)
	else:
		write_to_file_with_new_line_and_dt("udp data received from untrusted controller ip/port: {}; data: {}".format(addr, data), log_fname)
		continue
	# 2 - get queue status
	if data.startswith(b"queue_status"):
		sock.sendto(b"OK", addr)
	# 3 - ntpdate based on ntp (ip/fqdn) address from controller
	elif data.startswith(b"ntpupdate"):
		data = data.decode()
		ntp_server = data.split()[1]
		res = ntpupdate(ntp_server)
		if res:
			sock.sendto(b"OK", addr)
		else:
			sock.sendto(b"FAIL", addr)
	# 4 - process starting
	elif data.startswith(b"start_process_in_time"):
		data = data.decode()
		stime_list = data.split()[1:]
		stime = " ".join(stime_list)
		if check_start_time(stime):
			sock.sendto(b"OK", addr)
			start_process_in_time(stime)
		else:
			sock.sendto(b"FAIL", addr)