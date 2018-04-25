

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import service_now_apis
import time
import requests
import os
os.chdir("/bootflash/PCW_Demo")

from cli import cli

from config import SNOW_ADMIN, SNOW_DEV, SNOW_PASS, SNOW_URL

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


# read the syslog entry that triggered the event
syslog_input = cli("show logging | in %PLATFORM_FEP-1-FRU_PS_SIGNAL_FAULTY")
syslog_lines = syslog_input.split("\n")
lines_no = len(syslog_lines) - 2
syslog_info = syslog_lines[lines_no]


# retrieve the device hostname and S/N
device_name = cli("show run | in hostname")
device_sn = cli("sh ver | in System Serial Number")


# retrieve the device location
dnac_token = dnac_apis.get_dnac_jwt_token()
location = dnac_apis.get_device_location(device_name, dnac_token)


# define the incident description and comment
short_description = "Redundant Power Supply Failure - IOS XE Automation"
comment = "The device with the " + device_name + "\n has detected a Redundant Power Supply failure"
comment += "\n\nThe device SN is: " + device_sn
comment += "\n\nThe device location is " + location
comment += "\n\nSyslog: " + syslog_info + "\n\nSwitch Beacon LED turned ON"


# create a new ServiceNow incident
incident = service_now_apis.create_incident(short_description, comment, SNOW_DEV, 1)


# write the new incident name to file in /bootflash/PCW_Demo
incident_file = open("/bootflash/PCW_Demo/power_ticket.txt", "w")
incident_file.write(incident)
incident_file.close()

time.sleep(1)


# turn on the blue beacon LED on the device
cli("configure terminal\nhw-module beacon on switch 1")

print("End Application Run Power Supply Failure")
