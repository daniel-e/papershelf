import pygtk
pygtk.require('2.0')
import gtk

class DialogCorrect(gtk.Dialog):

  def __init__(self, title, parent, flag, values):
    gtk.Dialog.__init__(self, title, parent, flag)
    t = gtk.Table(rows = 3, columns = 2)
    t.set_col_spacings(10)
    t.set_row_spacings(10)

    l = gtk.Label("Filename:")
    l.set_alignment(xalign = 1.0, yalign = 0.5)
    t.attach(l, 0, 1, 0, 1)
    l.show()
    l = gtk.Label(values["filename"])
    l.set_alignment(xalign = 0.0, yalign = 0.5)
    t.attach(l, 1, 2, 0, 1)
    l.show()

    l = gtk.Label("Location:")
    l.set_alignment(xalign = 1.0, yalign = 0.5)
    t.attach(l, 0, 1, 1, 2)
    l.show()
    l = gtk.Label(values["path"])
    l.set_alignment(xalign = 0.0, yalign = 0.5)
    t.attach(l, 1, 2, 1, 2)
    l.show()

    l = gtk.Label("Index entry:")
    l.set_alignment(xalign = 1.0, yalign = 0.5)
    t.attach(l, 0, 1, 2, 3)
    l.show()
    l = gtk.Entry()
    l.set_width_chars(len(values["idxentry"]) + 10)
    l.set_text(values["idxentry"])
    t.attach(l, 1, 2, 2, 3)
    l.show()

    self.vbox.pack_start(t)
    t.show()
    self.add_button("Ok", 1)
    self.add_button("Cancel", 2)
