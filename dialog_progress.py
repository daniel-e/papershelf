import pygtk
pygtk.require('2.0')
import gtk

class DialogProgress(gtk.Dialog):

  def __init__(self, title, parent, flag, item):
    gtk.Dialog.__init__(self, title, parent, flag)

    h = gtk.HBox(False, 0)
    h.show()

    l = gtk.Label("Progress (between 0 and 100):")
    l.show()
    h.pack_start(l, False, False, 5)

    e = gtk.Entry()
    e.set_width_chars(10)
    e.set_text(str(item.get_progress()))
    e.show()
    e.connect
    self.progress = e

    h.pack_start(e, False, False, 5)

    self.vbox.pack_start(h, expand = True, fill = True, padding = 5)

    # if enter is pressed in the entry response_id 1 is returned
    self.add_action_widget(e, 1)

    self.add_button("_Update", 1)
    self.add_button("_Cancel", 2)

  def get_progress(self):
    return int(self.progress.get_text())
