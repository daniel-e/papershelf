import pygtk
pygtk.require('2.0')
import gtk

class DialogTags(gtk.Dialog):

  def __init__(self, title, parent, flag, item, known_tags):
    gtk.Dialog.__init__(self, title, parent, flag)

    l = gtk.Label("Tags for file: " + item.filename())
    l.set_alignment(xalign = 0.0, yalign = 0.5)
    l.show()
    self.vbox.pack_start(l, False, False, 10)

    sep = gtk.HSeparator()
    sep.show()
    self.vbox.pack_start(sep, False, False, 0)

    l = gtk.Label("Existing tags:")
    l.set_alignment(xalign = 0.0, yalign = 0.5)
    l.show()
    self.vbox.pack_start(l, False, False, 5)

    l = self.add_known_tags(known_tags, item)
    self.check_tags = l
    self.vbox.pack_start(l, False, False, 10)

    sep = gtk.HSeparator()
    sep.show()
    self.vbox.pack_start(sep, False, False, 0)

    l = gtk.Label("Define new tags (comma separated):")
    l.set_alignment(xalign = 0.0, yalign = 0.5)
    l.show()
    self.vbox.pack_start(l, False, False, 10)

    l = gtk.Entry()
    l.set_width_chars(40)
    l.set_alignment(xalign = 0.0)
    l.show()
    self.tags = l

    self.vbox.pack_start(l)

    self.add_button("Update", 1)
    self.add_button("Cancel", 2)

  def get_tags(self):
    r = [i.lower().strip() for i in self.tags.get_text().split(",")]
    for i in self.check_tags.get_children():
      if i.get_active():
        r.append(i.get_label())
    k = []
    for i in r:
      if len(i) > 0:
        k.append(i)
    return list(set(k))

  def add_known_tags(self, tags, item):
    item_tags = set(item.get_tags())
    n = len(tags)

    t = gtk.Table(rows = 1, columns = 1, homogeneous = True)
    t.set_col_spacings(10)
    t.show()

    cols = 3
    rows = int( n / cols)
    if n % cols != 0:
      rows += 1
    t.resize(max(rows, 1), cols)

    for i, tag in enumerate(tags):
      y = int(i / cols)
      x = i % cols
      c = gtk.CheckButton(tag)
      c.set_alignment(xalign = 0.0, yalign = 0.5)
      if tag in item_tags:
        c.set_active(True)
      c.show()
      #c.set_active(self.tag_visibility[tag])
      #c.connect("toggled", self.tag_toggled, tag)
      #self.tag_boxes.pack_start(c, False, False, 0)

      t.attach(c, x, x + 1, y, y + 1, xoptions = gtk.FILL)
    return t
