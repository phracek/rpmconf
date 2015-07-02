#!/usr/bin/env python3
#
# pylint: disable=missing-docstring,too-many-arguments,too-many-branches
#
# Copyright (C) 2015 Petr Hracek <phracek@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Red Hat trademarks are not licensed under GPLv3. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.

import os
from gi.repository import Gtk, Gdk
from rpmconf.rpmconf import RpmConf
GLADE_FILE = os.path.join(os.path.dirname(__file__), 'rpmconf-gui.glade')

class RpmConfGui(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GLADE_FILE)
        self.main_window = self.builder.get_object("main_window")
        self.list_view = self.builder.get_object("list_view")
        self.main_handlers = {
            "on_ok_btn_clicked": self.ok_btn_clicked,
            "on_main_window_delete_event": self.delete_event,
        }
        self.builder.connect_signals(self.main_handlers)
        self.store = Gtk.ListStore(str, str)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Changed configuration files", renderer, text=0)
        self.list_view.append_column(column)
        self.list_view.freeze_child_notify()
        self.list_view.set_model(None)
        #self.list_view.set_fixed_height_mode(True)
        rpmconf = RpmConf()
        conf_files = []
        for index, pkg in enumerate(rpmconf.packages):
            for pkg_hdr in pkg:
                for conf_file in rpmconf.get_list_of_config(pkg_hdr):
                    # XOrg crashed in case of uncommenting this row
                    # self.store.append([conf_file])
                    tmp = "{}.{}"
                    tmp_file = tmp.format(conf_file, "rpmnew")
                    if os.access(tmp_file, os.F_OK):
                        self.store.append([conf_file, tmp_file])
                    tmp_file = tmp.format(conf_file, "rpmsave")
                    if os.access(tmp_file, os.F_OK):
                        self.store.append([conf_file, tmp_file])
                    tmp_file = tmp.format(conf_file, "rpmorig")
                    if os.access(tmp_file, os.F_OK):
                        self.store.append([conf_file, tmp_file])

        self.list_view.set_model(self.store)
        self.list_view.thaw_child_notify()

        self.main_window.show_all()
        Gtk.main()

    def ok_btn_clicked(self, widget, event):
        Gtk.main_quit()

    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()

