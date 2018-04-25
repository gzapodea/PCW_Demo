

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


# the syslog entry that triggered the event
syslog_info = "%LINK-3-UPDOWN: Interface GigabitEthernet1/0/1, changed state to up"


# retrieve the device hostname and S/N
device_name = cli("show run | in hostname")


# define the incident description and comment
update_comment = "The device with the " + device_name + "\n has recovered from the Uplink failure"
update_comment += "\n\nSyslog: " + syslog_info


# find the existing ServiceNow incident
file = open("uplink_ticket.txt", "r")
incident = file.read()
file.close()


# update the ServiceNow incident
service_now_apis.update_incident(incident, update_comment, SNOW_DEV)


# close ServiceNow incident
time.sleep(1)
service_now_apis.close_incident(incident, SNOW_DEV)


# delete the incident name from the file in /bootflash/PCW_Demo
incident_file = open("/bootflash/PCW_Demo/uplink_ticket.txt", "w")
incident_file.write("INCIDENT")
incident_file.close()


print("End Application Run Uplink Interface Restored")
