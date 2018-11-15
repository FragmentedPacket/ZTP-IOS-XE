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

# This function checks if a CSR1000V router requires software upgrades
def csr1000v_upgrade_required():
    # Sleep for 5 seconds
    time.sleep(5)
    # Obtains show version output
    sh_version = cli('show version')
    # Check if on approved code
    match = re.search('Cisco IOS XE Software, Version 16.08.02a', sh_version)
    # Returns False if on approved version or True if upgrade is required
    if match:
        return False
    else:
        return True

# This function starts the process for a CSR1000V software upgrade
def csr1000v_upgrade_init():
    print "\n\n *** Upgrade of software is required. Beginning upgrade process... *** \n\n"

# This function checks if an ASR1001X router requires software upgrades
def asr1001x_upgrade_required():
    # Sleep for 5 seconds
    time.sleep(5)
    # Obtains show version output
    sh_version = cli('show version')
    # Check if on approved code
    match = re.search('Cisco IOS XE Software, Version 16.08.01a', sh_version)
    # Returns False if on approved version or True if upgrade is required
    if match:
        return False
    else:
        return True

# This function starts the process for an ASR1001X software upgrade
def asr1001x_upgrade_init():
    print "\n\n *** Upgrade of software is required. Beginning upgrade process... *** \n\n"

# This function checks if an ISR4431 router requires software upgrades
def isr4431_upgrade_required():
    # Sleep for 5 seconds
    time.sleep(5)
    # Obtains show version output
    sh_version = cli('show version')
    # Check if on approved code
    match = re.search('Cisco IOS XE Software, Version 16.08.01a', sh_version)
    # Returns False if on approved version or True if upgrade is required
    if match:
        return False
    else:
        return True

# This function starts the process for an ISR4431 software upgrade
def isr4431_upgrade_init():
    print "\n\n *** Upgrade of software is required. Beginning upgrade process... *** \n\n"

# This function checks if an ISR4451 router requires software upgrades
def isr4451_upgrade_required():
    # Sleep for 5 seconds
    time.sleep(5)
    # Obtains show version output
    sh_version = cli('show version')
    # Check if on approved code
    match = re.search('Cisco IOS XE Software, Version 16.08.01a', sh_version)
    # Returns False if on approved version or True if upgrade is required
    if match:
        return False
    else:
        return True

# This function starts the process for an ISR4451 software upgrade
def isr4451_upgrade_init():
    print "\n\n *** Upgrade of software is required. Beginning upgrade process... *** \n\n"

# This function checks if a 9500 Series switch requires software upgrades
def c95xx_upgrade_required():
    # Sleep for 5 seconds
    time.sleep(5)
    # Obtains show version output
    sh_version = cli('show version')
    # Check if on approved code
    match = re.search('Cisco IOS XE Software, Version 16.08.01a', sh_version)
    # Returns False if on approved version or True if upgrade is required
    if match:
        return False
    else:
        return True

# This function starts the process for a Catalyst 9500 software upgrade
def c95xx_upgrade_init():
    print "\n\n *** Upgrade of software is required. Beginning upgrade process... *** \n\n"

# This function checks if a 9300 Series switch requires software upgrades
def c93xx_upgrade_required():
    # Sleep for 5 seconds
    time.sleep(5)
    # Obtains show version output
    sh_version = cli('show version')
    # Check if on approved code
    match = re.search('Cisco IOS XE Software, Version 16.06.03', sh_version)
    # Returns False if on approved version or True if upgrade is required
    if match:
        return False
    else:
        return True

# This function starts the process for a Catalyst 9300 software upgrade
def c93xx_upgrade_init():
    print "\n\n *** Upgrade of software is required. Beginning upgrade process... *** \n\n"

# This function checks if a 3800 Series switch requires software upgrades
def c38xx_upgrade_required():
    # Sleep for 5 seconds
    time.sleep(5)
    # Obtains show version output
    sh_version = cli('show version')
    # Check if on approved code
    match = re.search('Cisco IOS XE Software, Version 16.06.04a', sh_version)
    # Returns False if on approved version or True if upgrade is required
    if match:
        return False
    else:
        return True

# This function starts the process for a Catalyst 3800 software upgrade
def c38xx_upgrade_init():
    print "\n\n *** Upgrade of software is required. Beginning upgrade process... *** \n\n"

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

# Get the platform type out of XML parsed inventory
# We need this in main function to call appropriate config and code
PLATFORM = get_platform()

def main():
    if 'CSR1000V' in PLATFORM:
        print "\n\n *** This is a CSR1000V *** \n\n"
        base_config()
        # Check to see if a platform software upgrade is required for CSR1000V
        UPGRADECHECK = csr1000v_upgrade_required()
        if UPGRADECHECK == True:
            csr1000v_upgrade_init()
        else:
            print "\n\n *** Software upgrade is not required. *** \n\n"
    elif 'ASR1001-X' in PLATFORM:
        print "\n\n *** This is an ASR1001-X *** \n\n"
        base_config()
        # Check to see if a platform software upgrade is required for ASR1001X
        UPGRADECHECK = asr1001x_upgrade_required()
        if UPGRADECHECK == True:
            asr1001x_upgrade_init()
        else:
            print "\n\n *** Software upgrade is not required. *** \n\n"
    elif 'ISR4431' in PLATFORM:
        print "\n\n *** This is an ISR4431 *** \n\n"
        base_config()
        # Check to see if a platform software upgrade is required for ISR4431
        UPGRADECHECK = isr4431_upgrade_required()
        if UPGRADECHECK == True:
            isr4431_upgrade_init()
        else:
            print "\n\n *** Software upgrade is not required. *** \n\n"
    elif 'ISR4451' in PLATFORM:
        print "\n\n *** This is an ISR4451 *** \n\n"
        base_config()
        # Check to see if a platform software upgrade is required for ISR4451
        UPGRADECHECK = isr4451_upgrade_required()
        if UPGRADECHECK == True:
            isr4451_upgrade_init()
        else:
            print "\n\n *** Software upgrade is not required. *** \n\n"
    elif 'c95xx Stack' in PLATFORM:
        print "\n\n *** This is a Catalyst 9500 Series Device *** \n\n"
        base_config()
        # Check to see if a platform software upgrade is required for Catalyst 9500 Series
        UPGRADECHECK = c95xx_upgrade_required()
        if UPGRADECHECK == True:
            c95xx_upgrade_init()
        else:
            print "\n\n *** Software upgrade is not required. *** \n\n"
    elif 'c93xx Stack' in PLATFORM:
        print "\n\n *** This is a Catalyst 9300 Series Device *** \n\n"
        base_config()
        # Check to see if a platform software upgrade is required for Catalyst 9300 Series
        UPGRADECHECK = c93xx_upgrade_required()
        if UPGRADECHECK == True:
            c93xx_upgrade_init()
        else:
            print "\n\n *** Software upgrade is not required. *** \n\n"
    elif 'c38xx Stack' in PLATFORM:
        print "\n\n *** This is a Catalyst 3800 Series Device *** \n\n"
        base_config()
        # Check to see if a platform software upgrade is required for Catalyst 3800 Series
        UPGRADECHECK = c38xx_upgrade_required()
        if UPGRADECHECK == True:
            c38xx_upgrade_init()
        else:
            print "\n\n *** Software upgrade is not required. *** \n\n"
    else:
        print "\n\n *** UNABLE TO DETECT PLATFORM. BASE CONFIG ONLY APPLIED *** \n\n"
        base_config()

main()

if __name__ == "__main__":
    main()
