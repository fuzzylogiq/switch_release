#!/usr/bin/env python
# encoding: utf-8
"""
switch_release.py

!!DESCRIPTION GOES HERE!!

Copyright (C) University of Oxford 2018
    Ben Goodstein <ben.goodstein at it.ox.ac.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import jss
import subprocess

EXT_ATTR = '43'
CHANNELS = ('Stable', 'Testing', 'Unstable')

def make_selection():
    selected = raw_input("Select release channel to switch to: ")
    try:
        selected = int(selected)
    except ValueError:
        print "Select from the options above."
        return make_selection()
    if selected < 1 or selected > len(CHANNELS):
        print "Select from the options above."
        return make_selection()
    return selected

j = jss.JSS(jss.JSSPrefs())
udid = subprocess.check_output("system_profiler SPHardwareDataType | awk '/UUID/ { print $3; }'", shell=True)

for num, channel in enumerate(CHANNELS, 1):
    print '{}. {}'.format(num, channel)

selected = make_selection()
new_channel = CHANNELS[selected - 1]

c = j.Computer('udid=%s' % udid)
v = c.find('extension_attributes/extension_attribute/[id="%s"]/value' % EXT_ATTR)
old_channel = v.text
v.text = new_channel
c.save()
print "Switched from {} to {}".format(old_channel, new_channel)
