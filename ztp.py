from cli import configure, configurep, cli, pnp
from xml.dom import minidom
import re
import json
import urllib2
import time

# Set variables for local usernames and secret password.
# Ansible will update these after bootstrap.
USER="ansible"
PASS="ztplab"
SECRET="ztplab"

# Set variables for FTP username and password.
# This is used to download code from FTP server if upgrade required
FTPUSER="ansible"
FTPPASS="ztplab"

# These variables will define the desired standard image filenames
# These are platform specific.
IMG_CSR1000V="csr1000v-universalk9.16.08.01a.bin"
IMG_ASR1001X="asr1001x-universalk9.16.08.01.SPA.bin"
IMG_ISR4431="isr4300-universalk9.16.08.01.SPA.bin"
IMG_ISR4451="isr4400-universalk9.16.08.01.SPA.bin"
IMG_C95XX="cat9k_iosxe.16.08.01a.SPA.bin"
IMG_C93XX="cat9k_iosxe.16.06.03.SPA.bin"
IMG_C38XX="cat3k_caa-universalk9.16.06.04a.SPA.bin"

def base_config():
    print "\n\n *** Setting hostname *** \n\n"
    configure('hostname ZTP-Success')
    print "\n\n *** Configuring local ansible user and enable secret *** \n\n"
    configure('username {} privilege 15 password {}'.format(USER,PASS))
    configure('enable secret {}'.format(SECRET))
    print "\n\n *** Configuring FTP user and pass for code retrieval *** \n\n"
    configure('ip ftp username {}'.format(FTPUSER))
    configure('ip ftp password {}'.format(FTPPASS))
    print "\n\n *** Setting vty logins to authenticate locally *** \n\n"
    configurep(['line vty 0 4', 'login local'])


def get_platform():
    # xml formatted output for show inventory
    inventory = cli('show inventory | format')
    # skip leading newline
    doc = minidom.parseString(inventory[1:])
    PLATFORM =[]
    for node in doc.getElementsByTagName('InventoryEntry'):
        # What if there are several devices?
        chassis = node.getElementsByTagName('ChassisName')[0]
        # This match should catch most routers - ISR, ASR, CSR1000V
        if "Chassis" in chassis.firstChild.data:
            PLATFORM.append(node.getElementsByTagName('PID')[0].firstChild.data)
        # This match will catch anything Catalyst 9500 Series
        elif "c95xx Stack" in chassis.firstChild.data:
            PLATFORM.append(node.getElementsByTagName('PID')[0].firstChild.data)
        # This match will catch anything Catalyst 9300 Series
        elif "c93xx Stack" in chassis.firstChild.data:
            PLATFORM.append(node.getElementsByTagName('PID')[0].firstChild.data)
        # This match will catch anything Catalyst 3800 Series
        elif "c38xx Stack" in chassis.firstChild.data:
            PLATFORM.append(node.getElementsByTagName('PID')[0].firstChild.data)
    return PLATFORM


def check_upgrade(model):
    # Sleep for 5 seconds
    time.sleep(5)
    # Obtains show version output
    sh_version = cli('show version')
    if 'CSR1000V' in model:
        match = re.search('Cisco IOS XE Software, Version 16.08.02a', sh_version)
        # Returns False if on approved version or True if upgrade is required
        if match:
            return False
        else:
            return True
    elif 'ASR1001-X' in model:
        match = re.search('Cisco IOS XE Software, Version 16.08.01a', sh_version)
        # Returns False if on approved version or True if upgrade is required
        if match:
            return False
        else:
            return True
    elif 'ISR4431' in model:
        match = re.search('Cisco IOS XE Software, Version 16.08.01a', sh_version)
        # Returns False if on approved version or True if upgrade is required
        if match:
            return False
        else:
            return True
    elif 'ISR4451' in model:
        match = re.search('Cisco IOS XE Software, Version 16.08.01a', sh_version)
        # Returns False if on approved version or True if upgrade is required
        if match:
            return False
        else:
            return True
    elif 'c95xx Stack' in model:
        match = re.search('Cisco IOS XE Software, Version 16.08.01a', sh_version)
        # Returns False if on approved version or True if upgrade is required
        if match:
            return False
        else:
            return True
    elif 'c93xx Stack' in model:
        match = re.search('Cisco IOS XE Software, Version 16.06.03', sh_version)
        # Returns False if on approved version or True if upgrade is required
        if match:
            return False
        else:
            return True
    elif 'c38xx Stack' in model:
        match = re.search('Cisco IOS XE Software, Version 16.06.04a', sh_version)
        # Returns False if on approved version or True if upgrade is required
        if match:
            return False
        else:
            return True


def main():
    PLATFORM = get_platform()
    model = PLATFORM[0]
    if check_upgrade(model):
        print "\n\n *** Upgrade of software is required. Beginning upgrade process... *** \n\n"
        upgrade_func()
    else:
        print "\n\n *** Software upgrade is not required. *** \n\n"

    base_config()


if __name__ == "__main__":
    main()