#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ver 1.3 by Petr V. Redkin

import datetime
import time
import socket
import subprocess
import json

log_fname = "synstart.log"
daemon_ip = '0.0.0.0'
daemon_port = 5555
controller_ip = ['192.168.1.179']
sleep_time = 1/1000 # 1 msec (1/1000 of second) default; change for more precision but higher CPU load

def convert_str_time_to_int(str_time):
	return int(str_time.replace(" ", "").replace(":", "").replace("-", "").replace("-", "").replace(".", ""))

def start_process_in_time(stime, daemon_starting_process):
	print("starting start_process_in_time: stime {}".format(stime))
	ln = len(stime)
	stime_to_compare = convert_str_time_to_int(stime)
	while True:
		actual_time = str(datetime.datetime.now())
		actual_time_to_compare = convert_str_time_to_int(actual_time[0:ln])
		if actual_time_to_compare >= stime_to_compare:
			res = subprocess.run(daemon_starting_process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
			print("finished start_process_in_time: stime {}, stime_to_compare {}, stime length {}, actual stime {}, actual actual_time_to_compare {} result {}".format(stime, stime_to_compare, ln, actual_time, actual_time_to_compare, res))
			return
		time.sleep(sleep_time)

def check_start_time(stime):
	print("starting check_start_time: stime {}".format(stime))
	ln = len(stime)
	stime_to_compare = convert_str_time_to_int(stime)
	actual_time = str(datetime.datetime.now())
	actual_time_to_compare = convert_str_time_to_int(actual_time[0:ln])
	if actual_time_to_compare >= stime_to_compare:
		res = False
		print("error check_start_time: scheduled starting time in the past!")
	else:
		res = True
	print("finished check_start_time: stime {}, stime_to_compare {}, stime length {}, actual stime {}, actual actual_time_to_compare {} result {}".format(stime, stime_to_compare, ln, actual_time, actual_time_to_compare, res))
	return res

def ntpupdate(ntp_server):
	print("starting ntpupdate: ntp_server {}".format(ntp_server))
	cmd = "sntp -S {}".format(ntp_server).split(" ")
	res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
	print("finished ntpupdate: ntp_server {}; result {}".format(ntp_server, res))
	if res.returncode == 0:
		return True
	else:
		return False


print("syn_start daemon started, expected time format for start_process_in_time function is \"{}\"".format(str(datetime.datetime.now())))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind ((daemon_ip,daemon_port))
while True:
	sock.listen(1)
	conn, addr = sock.accept()
	data = conn.recv(4096)
	# 1 - basic auth & request check
	if addr[0] in controller_ip:
		print("data received from trusted controller ip/port: {}; data: {}".format(addr, data))
		if b"command" not in data:
			print("no commands in data; skip request".format(addr, data))
			conn.send(b"FAIL")
			continue
		j = json.loads(data)
	else:
		print("data received from untrusted controller ip/port: {}; data: {}".format(addr, data))
		conn.send(b"FAIL")
		continue
	# 2 - get queue status
	if j["command"] == "queue_status":
		print("queue_status ok")
		conn.send(b"OK")
	# 3 - sntp based on ntp (ip/fqdn) address from controller
	elif j["command"] == "ntpupdate":
		data = data.decode()
		ntp_server = j["ip"]
		res = ntpupdate(ntp_server)
		if res:
			conn.send(b"OK")
		else:
			conn.send(b"FAIL")
	# 4 - process starting
	elif j["command"] == "start_process_in_time":
		data = data.decode()
		stime_list = data.split()[1:]
		stime = j["scheduled_start_time"]
		daemon_starting_process = j["daemon_starting_process"]
		if check_start_time(stime):
			conn.send(b"OK")
			start_process_in_time(stime, daemon_starting_process)
		else:
			conn.send(b"FAIL")
	else:
		print("unknown command; data {}".format(data))
		conn.send(b"FAIL")