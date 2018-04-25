

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import requests
import service_now_apis
import time
import os
os.chdir("/bootflash/PCW_Demo")

from cli import cli

from config import SNOW_ADMIN, SNOW_DEV, SNOW_PASS, SNOW_URL

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


# read the syslog entry that triggered the event
syslog_input = cli("show logging | in %PLATFORM_FEP-1-FRU_PS_SUSTAINED_OVERLOAD_RECOVERY:|%PLATFORM_FEP-1-FRU_PS_SIGNAL_OK:")
syslog_lines = syslog_input.split("\n")
lines_no = len(syslog_lines)-2
syslog_info = syslog_lines[lines_no]


# retrieve the device hostname and S/N
device_name = cli("show run | in hostname")
device_sn = cli("sh ver | in System Serial Number")


# define the incident description and comment
update_comment = "The device with the " + device_name + "\n has recovered from the Redundant Power Supply failure"
update_comment += "\n\nSyslog: " + syslog_info + "\n\nSwitch Beacon LED turned OFF"


# find the ServiceNow incident
file = open("power_ticket.txt", "r")
incident = file.read()
file.close()


# update the ServiceNow incident
service_now_apis.update_incident(incident, update_comment, SNOW_DEV)


# close ServiceNow incident
time.sleep(1)
service_now_apis.close_incident(incident, SNOW_DEV)


# delete the incident name from the file in /bootflash/PCW_Demo
incident_file = open("/bootflash/PCW_Demo/power_ticket.txt", "w")
incident_file.write("INCIDENT")
incident_file.close()


time.sleep(1)


# turn off the blue beacon LED on the device
cli("configure terminal\nhw-module beacon off switch 1")

print("End Application Run Power Supply Recovery")
