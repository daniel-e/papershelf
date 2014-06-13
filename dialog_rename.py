import pygtk
pygtk.require('2.0')
import gtk

class DialogRename(gtk.Dialog):

  def __init__(self, title, parent, flag, item):
    gtk.Dialog.__init__(self, title, parent, flag)

    h = gtk.HBox(False, 0)
    h.show()

    l = gtk.Label("Filename:")
    l.show()
    h.pack_start(l, False, False, 5)

    e = gtk.Entry()
    e.set_width_chars(60)
    e.set_text(item.filename())
    e.show()
    self.filename = e

    h.pack_start(e, False, False, 5)

    self.vbox.pack_start(h, expand = True, fill = True, padding = 5)

    self.add_button("Rename", 1)
    self.add_button("Cancel", 2)

  def get_new_filename(self):
    return self.filename.get_text()
