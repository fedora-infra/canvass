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
import flask, peewee, random, string
from flask import Flask, render_template, request, url_for, session, redirect
from database import *

__version__ = "0.0.0"

user_sessions = dict()

app = Flask("canvass")
app.secret_key = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(20))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method != 'POST':
        return "<h1>400 Bad Request</h1><br /><p>GET is not supported</p>"
    else:
        pass


@app.route('/api/submit_record', methods=['GET', 'POST'])
def api_submit_record():
    if request.method != 'POST':
        return "<h1>400 Bad Request</h1><br /><p>GET is not supported</p>"
    else:
        # ip = request.remote_addr

        country = "0"; # geolocate
        timezone = "0" # get TZ

        fields = {}
        # fields["ip"] = ip
        fields["country"] = request.form["country"]
        fields["timezone"] = request.form["timezone"]

        fields["total_storage"] = request.form['total_storage'] # GiB
        fields["total_memory"] = round(int(request.form['total_memory']), 0) # kB
        fields["linux_distro"] = request.form['linux_distro'] # e.g Fedora
        fields["linux_distro_version"] = request.form['linux_distro_version'] # e.g 21
        fields["linux_distro_name"] = request.form['linux_distro_name'] # e.g Twenty One
        fields["kernel_release"] = request.form['kernel_release'] # e.g 3.18.3-201.fc21.x86_64
        fields["cpus"] = request.form['cpus'] # e.g [' Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz', ' Intel(R) Core(TM) i5-4200U CPU @ 1.60GHz']
        fields["machine_arch"] = request.form['machine_arch'] # e.g x86_64
        fields["processor_arch"] = request.form['processor_arch'] # e.g x86_64
        fields["num_cpus"] = request.form['num_cpus'] # e.g 4

        print fields["total_memory"]
        try:
            insert_query = peewee.InsertQuery(Record, fields)
            insert_query.execute()
        except:
            return "500 Internal Server Error"
        return "200 OK"
