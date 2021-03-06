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
Stat Generation
Utility Functions
'''
import random
r = lambda: random.randint(0,255)

def gkp(counter):
    gfl_fkp = []

    for key, count in counter.iteritems():
        rcolor = ('#%02X%02X%02X' % (r(),r(),r()))
        gfl_fkp.append({
            "kname": key,
            "count": count,
            "rcolor": rcolor
        })
    return gfl_fkp
