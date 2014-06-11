import pygtk
pygtk.require('2.0')
import gtk

class DialogDetails(gtk.Dialog):

  def __init__(self, title, parent, flag, item, par):
    gtk.Dialog.__init__(self, title, parent, flag)
    self.resize(400, 200)
    self.parent_window = par

    t = gtk.Table(rows = 4, columns = 2, homogeneous = False)
    t.set_col_spacings(5)
    t.show()

    # ---
    l = gtk.Label("Abstract")
    l.show()
    l.set_alignment(xalign = 0.0, yalign = 0.0)
    t.attach(l, 0, 1, 0, 1)

    v = gtk.TextView()
    v.show()
    v.set_wrap_mode(gtk.WRAP_WORD)
    v.set_editable(True)
    v.set_cursor_visible(True)
    v.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 2)
    v.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 2)
    v.get_buffer().set_text(item.get_abstract())
    self.data_abstract = v

    sc = gtk.ScrolledWindow()
    sc.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
    sc.show()
    sc.add(v)
    t.attach(sc, 1, 2, 0, 1)

    # ---

    l, e = self.init_authors(item.get_authors())
    self.data_authors = e
    t.attach(l, 0, 1, 1, 2)
    t.attach(e, 1, 2, 1, 2)

    l, e = self.init_year(item.get_year())
    self.data_year = e
    t.attach(l, 0, 1, 2, 3)
    t.attach(e, 1, 2, 2, 3)

    l, e = self.init_title(item.get_title())
    self.data_title = e
    t.attach(l, 0, 1, 3, 4)
    t.attach(e, 1, 2, 3, 4)

    self.vbox.pack_start(t)

    self.add_button("Ok", 1)
    self.add_button("Cancel", 2)

  def init_authors(self, val):
    l = gtk.Label("Authors")
    l.show()
    l.set_alignment(xalign = 0.0, yalign = 0.5)

    e = gtk.Entry()
    e.set_width_chars(40)
    e.set_text(val)
    e.show()

    return l, e

  def init_year(self, val):
    l = gtk.Label("Year")
    l.show()
    l.set_alignment(xalign = 0.0, yalign = 0.5)

    e = gtk.Entry()
    e.set_width_chars(12)
    e.set_text(val)
    e.show()

    return l, e

  def init_title(self, val):
    l = gtk.Label("Title")
    l.show()
    l.set_alignment(xalign = 0.0, yalign = 0.5)

    e = gtk.Entry()
    e.set_width_chars(40)
    e.set_text(val)
    e.show()

    return l, e

  def get_title(self):
    return self.data_title.get_text()

  def get_authors(self):
    return self.data_authors.get_text()

  def get_year(self):
    return self.data_year.get_text()

  def get_abstract(self):
    buf = self.data_abstract.get_buffer()
    txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
    return txt
