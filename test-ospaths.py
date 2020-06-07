import os
import xml.dom.minidom
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('MateMenu', '2.0')
from gi.repository import GLib, Gtk, Gdk, GdkPixbuf

print("user data dir: " + GLib.get_user_data_dir())
print("user config dir: " + GLib.get_user_config_dir())
