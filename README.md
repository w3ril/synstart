Simple Python-based synchronization of program/utility launches between Linux systems.

![alt text](https://raw.githubusercontent.com/w3ril/synstart/main/synstart.png)

Usage:

1 - configure daemon mandatory variables (synstart_daemon.py):
   
   a) starting_process_cmd - a command that must be executed synchronously between daemons
   
   b) controller_ip - simple list of allowed controllers
   
2 - configure controller mandatory variables (synstart_controller.py):

  a) daemon_ip - list of daemons
  
  b) command - one of the implemented commands:
  
    1) b"ntpupdate 194.190.168.1" - system time synchronization 
    
    2) b"start_process_in_time 2021-02-01 19:58:00" - start time synchronization (utility/program)
    
    3) b"queue_status" - query the status of the queue (deamon status)
    
3 - start daemons

   ./synstart_daemon.py
  
4 - start controller

   ./synstart_controller.py
  
