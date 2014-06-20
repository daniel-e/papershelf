import pygtk
pygtk.require('2.0')
import gtk

import correct, settings, tools

class DialogDownload(gtk.Dialog):

  def __init__(self, title, parent, flag):
    gtk.Dialog.__init__(self, title, parent, flag)

    t = gtk.Table(rows = 4, columns = 2)
    t.set_col_spacings(10)

    l = gtk.Label("URL:")
    t.attach(l, 0, 1, 0, 1)
    l.show()
    self.url = gtk.Entry()
    self.url.set_width_chars(60)
    t.attach(self.url, 1, 2, 0, 1)
    self.url.show()

    l = gtk.Label("Title:")
    t.attach(l, 0, 1, 1, 2)
    l.show()
    self.pdftitle = gtk.Entry()
    t.attach(self.pdftitle, 1, 2, 1, 2)
    self.pdftitle.show()

    l = gtk.Label("Year:")
    t.attach(l, 0, 1, 2, 3)
    l.show()
    self.year = gtk.Entry(max = 10)
    t.attach(self.year, 1, 2, 2, 3)
    self.year.show()

    hb = gtk.HBox(False, 0)
    sep = gtk.VSeparator()
    sep.show()
    hb.pack_start(sep, True, True, 0)
    b = gtk.Button("Download PDF")
    b.connect("clicked", self.download, None)
    b.show()
    hb.pack_start(b, False, False, 0)
    hb.show()
    b = gtk.Button("Cancel")
    b.connect("clicked", self.cancel, None)
    b.show()
    hb.pack_start(b, False, False, 0)

    self.vbox.pack_start(t, False, False, 0)
    sep = gtk.VSeparator()
    sep.show()
    self.vbox.pack_start(sep, False, False, 5)
    self.vbox.pack_start(hb, False, False, 0)

    t.show()

  def cancel(self, widget, data = None):
    self.destroy()

  def download(self, widget, data = None):
    fname = tools.download_pdf(self.url.get_text())
    tools.extern_pdf_view(fname)

    shortname = tools.short_name(self.pdftitle.get_text())
    i = str(tools.next_number())
    shortname = i + "_" + shortname + "_p" + i + ".pdf"

    idxentry = self.pdftitle.get_text() + " (" + self.year.get_text() + ", p" + i + ")"

    s = settings.Settings()
    path = s.vars["pdflocation"]

    # DIALOG
    values = {"filename": shortname, "path": path, "idxentry": idxentry}
    dialog = dialogs.correct.DialogCorrect("Is this correct?", self.window, gtk.DIALOG_MODAL, values)
    r = dialog.run()
    dialog.destroy()

    if r == 1:
      d = path + "/" + shortname
      shutil.copy(f.name, d)
      os.execvp(s.PDF_VIEWER, [s.PDF_VIEWER, d])
