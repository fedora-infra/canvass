# -*- coding: utf-8 -*-
#
# Copyright © 2015 Chaoyi Zha <cydrobolt@fedoraproject.org>
#           © 2010 Fedora Unity Project (http://fedoraunity.org)
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
import os, sys, subprocess

def get_info(show_stderr = False, show_successful_cmds = True, show_failed_cmds = True):
    '''returns commonly requested (and some fedora-specific) system info'''
    # 'ps' output below has been anonymized: -n for uid vs username, and -c for short processname

    # cmd name, command, command2 fallback, command3 fallback, ...
    cmdlist = [
        ('OS Release',         '''lsb_release -ds''', '''cat /etc/*-release | uniq''', 'cat /etc/issue', 'cat /etc/motd'),
        ('Kernel',             '''uname -r ; cat /proc/cmdline'''),
        ('Desktop(s) Running', '''ps -eo comm= | grep -E '(gnome-session|startkde|startactive|xfce.?-session|fluxbox|blackbox|hackedbox|ratpoison|enlightenment|icewm-session|od-session|wmaker|wmx|openbox-lxde|openbox-gnome-session|openbox-kde-session|mwm|e16|fvwm|xmonad|sugar-session|mate-session)' '''),
        ('Desktop(s) Installed', '''ls -m /usr/share/xsessions/ | sed 's/\.desktop//g' '''),
        ('SELinux Status',      '''sestatus''', '''/usr/sbin/sestatus''', '''getenforce''', '''grep -v '^#' /etc/sysconfig/selinux'''),
        ('SELinux Error Count', '''selinuxenabled && journalctl --since yesterday |grep avc: |grep -Eo "comm=\"[^ ]+" |sort |uniq -c |sort -rn'''),
        ('CPU Model',          '''grep 'model name' /proc/cpuinfo | awk -F: '{print $2}' | uniq -c | sed -re 's/^ +//' ''', '''grep 'model name' /proc/cpuinfo'''),
        ('64-bit Support',     '''grep -q ' lm ' /proc/cpuinfo && echo Yes || echo No'''),
        ('Hardware Virtualization Support', '''grep -Eq '(vmx|svm)' /proc/cpuinfo && echo Yes || echo No'''),
        ('Load average',       '''uptime'''),
        ('Memory usage',       '''free -m''', 'free'),
        #('Top',                '''top -n1 -b | head -15'''),
        ('Top 5 CPU hogs',     '''ps axuScnh | awk '$2!=''' + str(os.getpid()) + '''' | sort -rnk3 | head -5'''),
        ('Top 5 Memory hogs',  '''ps axuScnh | sort -rnk4 | head -5'''),
        ('Disk space usage',   '''df -hT''', 'df -h', 'df'),
        ('Block devices',      '''blkid''', '''/sbin/blkid'''),
        ('PCI devices',        '''lspci''', '''/sbin/lspci'''),
        ('USB devices',        '''lsusb''', '''/sbin/lsusb'''),
        ('DRM Information',    '''grep drm /var/log/dmesg'''),
        ('Xorg modules',       '''grep LoadModule /var/log/Xorg.0.log | cut -d \\" -f 2 | xargs'''),
        ('GL Support',         '''glxinfo | grep -E "OpenGL version|OpenGL renderer"'''),
        ('Xorg errors',        '''grep '^\[.*(EE)' /var/log/Xorg.0.log'''),
        ('Kernel buffer tail', '''dmesg | tail'''),
        ('Last few reboots',   '''last -x -n10 reboot runlevel'''),
        ('YUM Repositories',   '''yum -C repolist''', '''ls -l /etc/yum.repos.d''', '''grep -v '^#' /etc/yum.conf'''),
        ('YUM Extras',         '''yum -C list extras'''),
        ('Last 20 packages installed', '''rpm -qa --nodigest --nosignature --last | head -20''')]
        #('Installed packages', '''rpm -qa --nodigest --nosignature | sort''', '''dpkg -l''') ]
    si = []

    for cmds in cmdlist:
        cmdname = cmds[0]
        cmd = ""
        for cmd in cmds[1:]:
            sys.stderr.write('.') # simple progress feedback
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = p.communicate()
            if p.returncode == 0 and out:
                break
            else:
                if show_stderr:
                    print >> sys.stderr, "sysinfo Error: the cmd \"%s\" returned %d with stderr: %s" % (cmd, p.returncode, err)
                    print >> sys.stderr, "Trying next fallback cmd..."
        if out:
            if show_successful_cmds:
                si.append( ('%s (%s)' % (cmdname, cmd), out) )
            else:
                si.append( ('%s' % cmdname, out) )
        else:
            if show_failed_cmds:
                si.append( ('%s (failed: "%s")' % (cmdname, '" AND "'.join(cmds[1:])), out) )
            else:
                si.append( ('%s' % cmdname, out) )

    sistr = "=== fpaste %s System Information (fpaste --sysinfo) ===\n"
    for cmdname, output in si:
        sistr += "* %s:\n" % cmdname
        if not output:
            sistr += "     N/A\n\n"
        else:
            for line in output.split('\n'):
                sistr += "     %s\n" % line

    return sistr
