import pygtk
pygtk.require('2.0')
import gtk
import gobject, os, tempfile

class DialogNotes(gtk.Dialog):

  def __init__(self, title, parent, flag, item, par):
    gtk.Dialog.__init__(self, title, parent, flag)
    self.resize(600, 600)
    self.parent_window = par

    a = self.get_action_area()

    v = gtk.TextView()
    v.show()
    v.set_wrap_mode(gtk.WRAP_WORD)
    v.set_editable(True)
    v.set_cursor_visible(True)
    v.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 2)
    v.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 2)
    v.get_buffer().set_text(item.get_notes())
    v.get_buffer().connect("changed", self.changed)
    self.v = v

    sc = gtk.ScrolledWindow()
    sc.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
    sc.show()
    sc.add(v)

    self.vbox.pack_start(sc)

    h = gtk.HBox(False, 0)
    h.show()

    self.modified_label = gtk.Label("")
    self.modified_label.show()
    h.pack_start(self.modified_label, False, False, 0)

    self.tmpfile = gtk.Label("")
    self.tmpfile.show()
    h.pack_start(self.tmpfile, False, False, 0)

    self.vbox.pack_end(h, expand = False, fill = False)


    b = gtk.Button("Save")
    b.show()
    b.connect("clicked", self.save_notes, item)
    a.pack_start(b, False, False, 0)
    b = gtk.Button("Close")
    b.show()
    b.connect("clicked", self.close, None)
    a.pack_start(b, False, False, 0)

    self.destroyed = False
    self.modified = False
    gobject.timeout_add(2000, self.auto_save)
    f = tempfile.NamedTemporaryFile(delete = False, suffix = ".papershelf")
    self.backup_file = f.name

  def close(self, widget, event, data = None):
    self.destroyed = True
    self.destroy()

  def save_notes(self, widget, item = None):
    self.modified_label.set_text("")
    buf = self.v.get_buffer()
    txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
    r = self.parent_window.pdfdb.update_notes(item, txt)
    if not r: # update failed
      # TODO
      pass

  def changed(self, widget, item = None):
    self.modified = True
    self.modified_label.set_text("modified  ")

  def auto_save(self):
    if not self.destroyed:
      if self.modified:
        self.save_in_tmpfile()
        self.modified = False
        self.tmpfile.set_text("(backup saved in " + self.backup_file + ")")
      gobject.timeout_add(2000, self.auto_save)

  def save_in_tmpfile(self):
    buf = self.v.get_buffer()
    txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter())

    f = open(self.backup_file + ".tmp", "w")
    f.write(txt)
    f.close()

    f = open(self.backup_file, "w")
    f.write(txt)
    f.close()

    os.unlink(self.backup_file + ".tmp")
