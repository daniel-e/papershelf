import pygtk
pygtk.require('2.0')
import gtk

class DialogFilename(gtk.Dialog):

  def __init__(self, title, parent, flag, button_label, path):
    gtk.Dialog.__init__(self, title, parent, flag)
    self.path = path

    h = gtk.HBox(False, 0)
    h.show()

    h.pack_start(gtk.Label("Filename:"), False, False, 5)

    self.filename = gtk.Entry()
    self.filename.set_width_chars(60)
    h.pack_start(self.filename, False, False, 5)

    b = gtk.Button("Choose")
    b.connect("clicked", self.choose_file, None)
    h.pack_start(b, False, False, 5)

    h.show_all()
    self.vbox.pack_start(h, expand = True, fill = True, padding = 5)

    self.add_button(button_label, gtk.RESPONSE_OK)
    self.add_button("Cancel", gtk.RESPONSE_CANCEL)

  def set_filename(self, fname):
    self.filename.set_text(fname)

  def get_filename(self):
    return self.filename.get_text()

  def choose_file(self, widget, data = None):
    f = gtk.FileChooserDialog(
      "Select a filename", self,
      buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
    )
    f.set_current_folder(self.path)
    if f.run() == gtk.RESPONSE_OK:
      self.set_filename(f.get_filename())
    f.destroy()
