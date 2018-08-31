# -*- coding: utf-8 -*-

# This plug-in was created for educational purposes. It was 
# created as part of a project for my dissertation. 
# Please feel free to download, use and edit.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import os
import os.path
from datetime import datetime, time
import dateutil.tz
import shutil
import glob

from docutils import nodes
from docutils.parsers.rst import Directive, directives
import lxml

from nikola.plugin_categories import RestExtension
from nikola.utils import LocaleBorg
from nikola import utils

class Plugin(RestExtension):

    name = "setup_event"

    def set_site(self, site):
        self.site = site
        Event.site = site
        directives.register_directive('setup_event', Event)
        return super(Plugin, self).set_site(site)
		
END_DATE = (u"""<div class="end_date">
<h1>{cd}</h1>
<p id="demo"></p>
<script>
document.getElementById("demo").innerHTML = 
"The full URL of this page is:<br>" + window.location.pathname;
</script>
</div>""")

EXP_DATE = (u"""<div class="expire_date">
<h1>EXPIRED!!</h1>
</div>""")

#schedule=True
#countDownDate = datetime.date('2018-07-20  1:00:00', '%Y-%m-%d %H:%M:%S')
#tz = dateutil.tz.tzlocal()
#today = now = datetime.datetime.now(tz)
#distance = abs(countDownDate - today)

def timeDifference(date1, date2):
  timedelta = date2 - date1
  if date2 < date1:
    return 0
  return timedelta.days * 24 * 3600 + timedelta.seconds

def Remaining(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return (days, hours, minutes, seconds)

#expireDate = datetime.strptime('2012-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')

class Event(Directive):
    """ Restructured text extension for inserting date and time in the correct format

        Usage:

        .. setup_event:: 2018-07-23 01:00:00
            :filename: <filename>
			
			Your review.
		
   """

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True	
    option_spec = {
        'countdown': directives.unchanged,
        'filename': directives.unchanged,
        'tr': directives.unchanged,
	}

    def run(self):
        """ Required by the Directive interface. Create docutils nodes """
        options = {
            'endDate': ' '.join(self.arguments),
            'filename': self.options.get('filename', ''),
            'cd': self.options.get('countdown', ''),
            'tr': self.options.get('tr', ''),
            'output_folder': self.site.config['OUTPUT_FOLDER'],
        }
        directory = os.path.join(options['output_folder'],'../expirePage')
        post = os.path.join(options['output_folder'],'../posts')
        filename = os.path.basename(os.path.join(post, options['filename']+".rst"))

        expireDate = datetime.strptime(options['endDate'], '%Y-%m-%d %H:%M:%S') #END_DATE.format(**options)
        today = datetime.now()
        countdown = "Time Remaining: %d days, %d hours, %d minutes, %d seconds" % Remaining(timeDifference(today, expireDate))

        if expireDate > today:
            options['cd'] = countdown
        else: 
            options['cd'] = 'EXPIRED!!'
            if not os.path.exists(directory):
                utils.makedirs(directory)
            for f in os.listdir(post):
                fn = os.path.join(post, f)
                name = os.path.basename(fn)
                if (os.path.isfile(fn)):
                    if (name == filename):
                        shutil.copy(fn, directory)
        return [nodes.raw('', END_DATE.format(**options), format='html')]