import pygtk
pygtk.require('2.0')
import gtk

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
    self.v = v

    sc = gtk.ScrolledWindow()
    sc.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
    sc.show()
    sc.add(v)

    self.vbox.pack_start(sc)

    b = gtk.Button("Save")
    b.show()
    b.connect("clicked", self.save_notes, item)
    a.pack_start(b, False, False, 0)
    b = gtk.Button("Close")
    b.show()
    b.connect("clicked", self.close, None)
    a.pack_start(b, False, False, 0)

  def close(self, widget, event, data = None):
    self.destroy()

  def save_notes(self, widget, item = None):
    buf = self.v.get_buffer()
    txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
    r = self.parent_window.pdfdb.update_notes(item, txt)
    if not r: # update failed
      # TODO
      pass
