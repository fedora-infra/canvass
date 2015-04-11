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
Canvass Main Client
'''

from __future__ import print_function
import platform, glob, re, os
from collections import OrderedDict

# System Info

system_uname = platform.uname()
linux_release = platform.linux_distribution()

machine_arch = system_uname[4]
processor_arch = system_uname[5]
kernel_release = system_uname[2]

linux_distro = linux_release[0]
linux_distro_version = linux_release[1]
linux_distro_name = linux_release[2]

# Hardware Info
'''
CPU
'''
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

'''
Memory
'''

meminfo=OrderedDict()

with open('/proc/meminfo') as f:
    for line in f:
        meminfo[line.split(':')[0]] = line.split(':')[1].strip()

# Total Memory in kB
total_memory = meminfo['MemTotal']

'''
Storage
'''

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

print(
    total_storage,
    total_memory,
    linux_distro,
    linux_distro_version,
    linux_distro_name,
    cpus,
    machine_arch,
    system_uname,
    processor_arch
)

# Upload data
