Simple Python-based synchronization of program/utility launches between Linux systems.

Synchronization of the start is achieved due to the scheduled start time on several UDP daemons/servers (similar to at/atd, but much more precise). Before syncing the start of the program/utility, do not forget to synchronize the time between daemons using "ntpupdate <ntp_server>" command, this requires the installed ntpdate utility.

By default, the start synchronization is expected to be up to 1 millisecond (excluding the desynchronization introduced by ntp), but tuning allows you to synchronize the start up to 10 microseconds. Example:

 - daemon1: actual stime 2021-02-01 22:34:00.000085
 
 - daemon2: actual stime 2021-02-01 22:34:00.000209
 
 - daemon3: actual stime 2021-02-01 22:34:00.000191

![alt text](https://raw.githubusercontent.com/w3ril/synstart/main/synstart.png)

Usage:

1 - configure daemon mandatory variables (synstart_daemon.py):
   
   a) controller_ip - simple list of allowed controllers
   
2 - configure controller mandatory variables (synstart_controller.py):

  a) daemon_ip - list of daemons
  
  b) daemon_starting_process - a command that must be executed synchronously between daemons
  
  c) daemon_command - one of the implemented commands:
  
    1) { "command": "ntpupdate", "ip": "194.190.168.1"} - system time synchronization, you need to provide ntp server (local, pool.ntp.org or other)
    
    2) { "command": "start_process_in_time", "scheduled_start_time": "2021-02-02 16:11:00", "daemon_starting_process": daemon_starting_process} - start time synchronization (utility/program)
    
    3) { "command": "queue_status" } - query the status of the queue (daemon status)
    
3 - start daemons

   ./synstart_daemon.py
  
4 - start controller

   ./synstart_controller.py
  
