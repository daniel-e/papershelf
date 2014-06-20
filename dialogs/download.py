import pygtk
pygtk.require('2.0')
import gtk

import shutil
import correct, settings, tools, filename

class DialogDownload(gtk.Dialog):

  def __init__(self, title, parent, flag, settings):
    gtk.Dialog.__init__(self, title, parent, flag)

    self.settings = settings

    self.create_input_mask()
    self.create_buttons()
    self.show_all()

  def create_buttons(self):
    b = gtk.Button("_Download PDF")
    b.connect("clicked", self.download, None)
    self.get_action_area().pack_end(b, False, False, 0)

    b = gtk.Button("_Cancel")
    b.connect("clicked", self.cancel, None)
    self.get_action_area().pack_end(b, False, False, 0)

  def create_input_mask(self):
    v = gtk.HBox(False, 5)
    v.pack_start(gtk.Label("URL to PDF:"), expand = False)

    self.url = gtk.Entry()
    self.url.set_width_chars(60)
    v.pack_start(self.url, expand = True)

    v.show_all()
    self.vbox.pack_start(v, False, False, 0)


  def cancel(self, widget, data = None):
    self.destroy()

  def download(self, widget, data = None):
    try:
      fname = tools.download_pdf(self.url.get_text())
    except:
      d = gtk.MessageDialog(
        None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
        gtk.BUTTONS_CLOSE, "Could not download file.")
      d.run()
      d.destroy()
      return

    tools.extern_pdf_view(fname)

    # ask the user whether the downloaded PDF is actually the PDF which he
    # wanted to be downloaded

    d = gtk.MessageDialog(
      None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION,
      gtk.BUTTONS_OK_CANCEL, "The PDF has been downloaded successfully. Is it displayed correctly?"
    )
    r = d.run()
    d.destroy()
    if r == gtk.RESPONSE_CANCEL:
      return

    self.select_filename(fname)

  def select_filename(self, tmpfname):
    path = self.settings.vars["pdflocation"]
    d = filename.DialogFilename("Select a filename", None, gtk.DIALOG_DESTROY_WITH_PARENT, "Ok", path)
    dst = path + "/" + tmpfname.split("/")[-1]
    d.set_filename(dst.replace("//", "/"))
    r = d.run()
    dstfname = d.get_filename()
    d.destroy()
    if r == gtk.RESPONSE_OK:
      if self.import_file(tmpfname, dstfname):
        self.destroy()
      else:
        self.select_filename(tmpfname)

  def import_file(self, src, dst):
    path = self.settings.vars["pdflocation"] + "/"
    path = path.replace("//", "/")

    d = dst.replace("//", "/").split("/")
    dstfname = d[-1]
    dstpath = "/".join(d[0:-1]) + "/"

    if dstpath != path:
      d = gtk.MessageDialog(
        None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION,
        gtk.BUTTONS_OK_CANCEL,
        "You have selected a folder which is not the folder where your imported PDFs are stored."
        "Therefore, the new PDF will not be recognized by papershelf.\n\n"
        "Do you want to continue?"
      )
      r = d.run()
      d.destroy()
      if r == gtk.RESPONSE_CANCEL:
        return False

    try:
      shutil.copy(src, dstpath + dstfname)
    except:
      raise
      d = gtk.MessageDialog(
        None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
        gtk.BUTTONS_OK, "Could not copy PDF into destination folder."
      )
      d.run()
      d.destroy()

    return True
