import pygtk
pygtk.require('2.0')
import gtk

class DialogDetails(gtk.Dialog):

  def __init__(self, title, parent, flag, item, par):
    gtk.Dialog.__init__(self, title, parent, flag)
    self.resize(1, 400)
    self.parent_window = par

    t = gtk.Table(rows = 4, columns = 2, homogeneous = False)
    t.set_col_spacings(5)
    t.show()

    # ---

    l, e = self.init_title(item.get_title())
    self.data_title = e
    t.attach(l, 0, 1, 0, 1, xoptions = gtk.SHRINK|gtk.FILL)
    t.attach(e, 1, 2, 0, 1, xoptions = gtk.FILL)

    l, e = self.init_authors(item.get_authors())
    self.data_authors = e
    t.attach(l, 0, 1, 1, 2, xoptions = gtk.SHRINK|gtk.FILL)
    t.attach(e, 1, 2, 1, 2, xoptions = gtk.FILL)

    l, e = self.init_year(item.get_year())
    self.data_year = e
    t.attach(l, 0, 1, 2, 3, xoptions = gtk.SHRINK|gtk.FILL)
    t.attach(e, 1, 2, 2, 3, xoptions = gtk.FILL)

    # ---

    f = gtk.Frame("")
    f.show()
    f.add(t)

    self.vbox.pack_start(f, expand = False, fill = False, padding = 0)

    # ---

    f = gtk.Frame("Abstract")
    f.show()

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
    b = gtk.VBox(False)
    b.show()
    b.pack_start(sc, padding = 5)

    f.add(b)

    self.vbox.pack_start(f, expand = True, fill = True, padding = 5)

    # ---

    self.add_button("Ok", 1)
    self.add_button("Cancel", 2)

  def init_authors(self, val):
    l = gtk.Label("Authors")
    l.show()
    l.set_alignment(xalign = 0.0, yalign = 0.5)

    e = gtk.Entry()
    e.set_width_chars(60)
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
    e.set_width_chars(60)
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
