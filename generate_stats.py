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
Generate static statistics page
Set on a daily cronjob to keep up to date
'''
from jinja2 import Environment, PackageLoader
from canvass.database import *
import time, peewee, canvass.config



countries = []
country_user_count = dict()


distro_records = Record.select().where(Record.linux_distro == canvass.config.distro)
for record in distro_records:
    '''
    Per-Release
    Distribution User Map
    '''
    if record.country not in country_user_count.keys():
        country_user_count[record.country] = 1
    else:
        country_user_count[record.country] += 1

for country, count in country_user_count.iteritems():
    countries.append({
        "country_code": country,
        "user_num": count
    })

env = Environment(loader=PackageLoader('canvass', 'templates'))
generated_date = (time.strftime("%d/%m/%Y at %I:%M"))
template = env.get_template('stats_overview.html')
compiled = template.render(
    generated_date=generated_date, countries=countries
)
static_stat_template = "{}{}{}".format(
    "{% extends \"base.html\" %}\n\n{% block body %}\n",
    compiled,
    "\n{% endblock %}"
)

f = open('canvass/templates/static_stat.html', 'w')
f.write(static_stat_template)
