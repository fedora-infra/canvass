# -*- coding: utf-8 -*-
#
# Copyright © 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

'''
Canvass Python Library
'''
from __future__ import print_function
import platform, glob, re, os, urllib, urllib2
import json, sysinfo
from collections import OrderedDict

def get_sysinfo():
    print( sysinfo.get_info() )

def submit_sysinfo():
    pass

get_sysinfo()




# Config

data_send_endpoint = "http://localhost:5000/api/submit_record"
geo_ip_endpoint = "https://geoip.fedoraproject.org/city"

# System Info
try:
    system_uname = platform.uname()
    linux_release = platform.linux_distribution()

    machine_arch = system_uname[4]
    processor_arch = system_uname[5]
    kernel_release = system_uname[2]

    linux_distro = linux_release[0]
    linux_distro_version = linux_release[1]
    linux_distro_name = linux_release[2]
except:
    print("Error gathering Linux information")
# Hardware Info
'''
CPU
'''
try:
    cpus = []
    with open('/proc/cpuinfo') as f:
        for line in f:
            # Ignore the blank line separating the information between
            # details about two processing units
            if line.strip():
                if line.rstrip('\n').startswith('model name'):
                    model_name = line.rstrip('\n').split(':')[1]
                    cpus.append(model_name)
    num_cpus = len(cpus)
except:
    print("Error gathering CPU information")

'''
Memory
'''

try:
    meminfo=OrderedDict()
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()

    # Total Memory in kB
    total_mem_int = re.match("([0-9]*).*?", meminfo["MemTotal"])
    total_memory = total_mem_int.group(0)
except:
    print("Error gathering memory information")

'''
Storage
'''
try:
    # Add any other device pattern to read from
    dev_pattern = ['sd.*','mmcblk*']
    storage_devices = []
    total_storage = 0

    def size(device):
        nr_sectors = open(device+'/size').read().rstrip('\n')
        sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')

        # The sect_size is in bytes, so we convert it to GiB and then send it back
        return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)

    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                storage_devices.append({"device": device, "size": size(device)})
    for sto_device in storage_devices:
        # size is in GiB
        total_storage += sto_device['size']
except:
    print("Error gathering storage information")
'''
print(
    total_storage,
    total_memory,
    linux_distro,
    linux_distro_version,
    linux_distro_name,
    cpus,
    machine_arch,
    processor_arch,
    num_cpus,
    kernel_release
)
'''
try:
    response_geoip = urllib2.urlopen(geo_ip_endpoint).read()
    geoip_object = json.loads(response_geoip)
    country = str(geoip_object["country_code"])
    timezone = str(geoip_object["time_zone"])
except:
    print("Error obtaining geolocation")
    country = "null"
    timezone = "null"

'''
* Upload Data *
urllib is used to reduce external dependencies
'''
try:
    values = {
        "total_storage": total_storage,
        "total_memory": total_memory,
        "linux_distro": linux_distro,
        "linux_distro_version": linux_distro_version,
        "linux_distro_name": linux_distro_name,
        "cpus": cpus,
        "machine_arch": machine_arch,
        "processor_arch": processor_arch,
        "num_cpus": num_cpus,
        "kernel_release": kernel_release,
        "country": country,
        "timezone": timezone
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(data_send_endpoint, data)
    response = urllib2.urlopen(req).read()
    if response == "200 OK":
        print("Success")
    else:
        print("Sent, but did not receive 200")
except:
    print("Could not send data")
