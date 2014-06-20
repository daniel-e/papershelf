import pygtk
pygtk.require('2.0')
import gtk

class DialogSettings(gtk.Dialog):

  def __init__(self, title, parent, flag, settings):
    gtk.Dialog.__init__(self, title, parent, flag)

    s = settings
    self.s = s

    t = gtk.Table(rows = 3, columns = 3)
    t.set_col_spacings(10)
    t.set_row_spacings(10)

    l = gtk.Label("PDF Viewer:")
    l.set_alignment(xalign = 1.0, yalign = 0.5)
    t.attach(l, 0, 1, 0, 1)
    l.show()
    l = gtk.Entry()
    l.set_width_chars(40)
    l.set_text(s.vars["pdfviewer"])
    l.set_alignment(xalign = 0.0)
    t.attach(l, 1, 2, 0, 1)
    l.show()
    self.pdf_viewer = l

    l = gtk.Label("PDF Location:")
    l.set_alignment(xalign = 1.0, yalign = 0.5)
    t.attach(l, 0, 1, 1, 2)
    l.show()
    l = gtk.Entry()
    l.set_width_chars(40)
    l.set_text(s.vars["pdflocation"])
    l.set_alignment(xalign = 0.0)
    t.attach(l, 1, 2, 1, 2)
    l.show()
    self.pdf_location = l
    b = gtk.Button("Choose")
    b.show()
    b.connect("clicked", self.choose_pdf_location, None)
    t.attach(b, 2, 3, 1, 2)


    # ----
    l = gtk.Label("Preview converter:")
    l.set_alignment(xalign = 1.0, yalign = 0.5)
    t.attach(l, 0, 1, 2, 3)
    l.show()
    l = gtk.Entry()
    l.set_width_chars(40)
    l.set_text(s.vars["pdfconvert"])
    l.set_alignment(xalign = 0.0)
    t.attach(l, 1, 2, 2, 3)
    l.show()
    self.pdf_convert = l
    b = gtk.Button("Choose")
    b.show()
    b.connect("clicked", self.choose_pdf_convert, None)
    t.attach(b, 2, 3, 2, 3)

    # ----
    self.vbox.pack_start(t)
    t.show()

    self.add_button("Ok", 1)
    self.add_button("Cancel", 2)

  def show(self):
    if self.run() == 1:
      s = self.s
      s.vars["pdfviewer"] = self.pdf_viewer.get_text()
      s.vars["pdflocation"] = self.pdf_location.get_text()
      s.vars["pdfconvert"] = self.pdf_convert.get_text()
      s.commit()
    self.destroy()

  def choose_pdf_location(self, widget, data = None):
    f = gtk.FileChooserDialog("Select a directory", self,
      buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    f.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
    r = f.run()
    if r == gtk.RESPONSE_OK:
      self.pdf_location.set_text(f.get_current_folder())
    f.destroy()

  def choose_pdf_convert(self, widget, data = None):
    f = gtk.FileChooserDialog("Select an executable", self,
      buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    #f.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
    r = f.run()
    if r == gtk.RESPONSE_OK:
      self.pdf_convert.set_text(f.get_filename())
    f.destroy()
