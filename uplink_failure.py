

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import service_now_apis
import dnac_apis
import time
import requests
import os
os.chdir("/bootflash/PCW_Demo")

from cli import cli

from config import SNOW_ADMIN, SNOW_DEV, SNOW_PASS, SNOW_URL

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


# syslog entry that triggered the event
syslog_info = "%LINK-3-UPDOWN: Interface GigabitEthernet1/0/1, changed state to down"


# retrieve the device hostname and S/N
device_name = cli("show run | in hostname")
device_sn = cli("sh ver | in System Serial Number")


# retrieve the device location from DNA Center
dnac_token = dnac_apis.get_dnac_jwt_token()
location = dnac_apis.get_device_location(device_name, dnac_token)


# define the incident description and comment
short_description = "Switch Uplink Down - IOS XE Automation"
comment = "The device with the " + device_name + "\n has detected an Uplink Interface Down"
comment += "\n\nThe device SN is: " + device_sn
comment += "\n\nThe device location is " + location
comment += "\n\nSyslog: " + syslog_info


# create a new ServiceNow incident
incident = service_now_apis.create_incident(short_description, comment, SNOW_DEV, 3)


# write the new incident name to file in /bootflash/PCW_DEMO
incident_file = open("/bootflash/PCW_Demo/uplink_ticket.txt", "w")
incident_file.write(incident)
incident_file.close()


print("End Application Run Uplink Interface Down")
