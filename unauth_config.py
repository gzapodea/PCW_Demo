

# developed by Gabi Zapodeanu, TSA, Global Partner Organization


from cli import cli
import time
import difflib
import requests
import json
import service_now_apis
import os
os.chdir("/bootflash/PCW_Demo")



from config import SNOW_URL, SNOW_DEV, SNOW_PASS

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth  # for Basic Auth

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


def save_config():

    # save running configuration, use local time to create new config file name
    output = cli('show run')
    filename = 'current_config'

    f = open(filename, "w")
    f.write(output)
    f.close

    return filename


def compare_configs(cfg1, cfg2):

    # compare two config files
    d = difflib.unified_diff(cfg1, cfg2)

    diffstr = ''
    for line in d:
        if line.find('Current configuration') == -1:
            if line.find('Last configuration change') == -1:
                if (line.find('+++') == -1) and (line.find('---') == -1):
                    if (line.find('-!') == -1) and (line.find('+!') == -1):
                       if line.startswith('+'):
                            diffstr = diffstr + '\n' + line
                       elif line.startswith('-'):
                            diffstr = diffstr + '\n' + line

    return diffstr


# main application

syslog_input = cli('show logging | in %SYS-5-CONFIG_I')
syslog_lines = syslog_input.split('\n')
lines_no = len(syslog_lines)-2
user_info = syslog_lines[lines_no]

# identify the diff between the running config and the baseline
old_cfg_fn = '/bootflash/PCW_Demo/base-config'
new_cfg_fn = save_config()

f = open(old_cfg_fn)
old_cfg = f.readlines()
f.close

f = open(new_cfg_fn)
new_cfg = f.readlines()
f.close

diff = compare_configs(old_cfg,new_cfg)
print diff

f = open('/bootflash/PCW_Demo/diff', 'w')
f.write(diff)
f.close

if diff != '':

    # retrieve the device hostname and S/N
    device_name = cli("show run | in hostname")
    device_sn = cli("sh ver | in System Serial Number")
    print('Hostname: ', device_name)

    # retrieve the device location from DNA Center
    dnac_token = dnac_apis.get_dnac_jwt_token()
    location = dnac_apis.get_device_location(device_name, dnac_token)

    # define the incident description and comment
    short_description = "Unauthorized Configuration Change - IOS XE Automation"
    comment = "The device with the " + device_name + "\n has detected an Unauthorized Configuration Change"
    comment += "\n\nThe device SN is: " + device_sn
    comment += "\n\nThe device location is " + location
    comment += "\n\nThe configuration changes are\n" + diff + "\n\nConfiguration changed by user: " + user_info

    # create ServiceNow incident
    incident = service_now_apis.create_incident(short_description, comment, SNOW_DEV, 1)

    # rollback configuration
    time.sleep(5)
    cli('configure replace flash:/PCW_Demo/base-config force')
    update_comment = "Configuration rollback to baseline - IOS XE Automation"
    service_now_apis.update_incident(incident, update_comment, SNOW_DEV)

print('End Application Run Unauthorized Configuration Change')
