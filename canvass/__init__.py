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
from flask_fas_openid import fas_login_required, cla_plus_one_required, FAS
from database import *

__version__ = "0.0.0"

user_sessions = dict()

app = Flask("canvass")
fas = FAS(app)
app.secret_key = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(20))
app.config['FAS_OPENID_ENDPOINT'] = 'http://id.fedoraproject.org/'
app.config['FAS_CHECK_CERT'] = True


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/post_auth', methods=['GET'])
@fas_login_required
def post_auth():
    session['logged'] = True
    return redirect(url_for('index'))

@app.route('/auth', methods=['GET'])
def auth_login():
    groups = config.admin_groups
    next_url = url_for('post_auth')
    return fas.login(return_url=next_url, groups=groups)

@app.route('/logout', methods=['GET'])
def logout():
    if flask.g.fas_user:
        fas.logout()
        session['logged'] = None
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET'])
@fas_login_required
def admin_panel():
    is_admin = False
    for admin_group in config.admin_groups:
        if admin_group in flask.g.fas_user.groups:
            is_admin = True
    if is_admin == True:
        return render_template("admin.html")
    else:
        render_template('error.html', error="Your account does not have access to this resource.")

@app.route('/stats/overview', methods=['GET'])
def stats_overview():
    # Send statically generated statistic files
    # Stats page needs to be generated using
    # generate_stats script. Set on cron cycle
    return render_template("static_stat.html")

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
