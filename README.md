Simple Python-based synchronization of program/utility launches between Linux systems.

Synchronization of the start is achieved due to the scheduled start time on several TCP daemons/servers (similar to at/atd, but much more precise). Before syncing the start of the program/utility, do not forget to synchronize the time between daemons using build-in ntpupdate command, this requires the installed sntp utility.

By default, the start synchronization is expected to be up to <b>1 millisecond</b> (excluding the desynchronization introduced by ntp), but tuning allows you to synchronize the start <b>up to 10 microseconds</b>.

Example:

<b>at/atd based (scheduled start at 20:32)</b>

- daemon1 actual start at: 20:32:00.160

- daemon2 actual start at: 20:32:00.894

<b>synstart based (scheduled start at 22:34)</b>

- daemon1 actual start at: 22:34:00.000085

- daemon2 actual start at: 22:34:00.000209

- daemon3 actual start at: 22:34:00.000191

![alt text](https://raw.githubusercontent.com/w3ril/synstart/main/synstart.png)

<b> Usage: </b>

<b> 1 - configure daemon mandatory variables (synstart_daemon.py): </b>
   
   a) controller_ip - simple list of allowed controllers
   
<b> 2 - configure controller mandatory variables (synstart_controller.py): </b>

  a) daemon_ip - list of daemons
  
  b) daemon_starting_process - a command that must be executed synchronously between daemons
  
  c) daemon_command - one of the implemented commands:
  
    1) { "command": "ntpupdate", "ip": "194.190.168.1"} - system time synchronization, you need to provide ntp server (local, pool.ntp.org or other)
    
    2) { "command": "start_process_in_time", "scheduled_start_time": "2021-02-02 16:11:00", "daemon_starting_process": daemon_starting_process} - start time synchronization (utility/program)
    
    3) { "command": "queue_status" } - query the status of the queue (daemon status)
    
<b> 3 - start daemons </b>

   ./synstart_daemon.py
  
<b> 4 - start controller </b>

   ./synstart_controller.py
  
