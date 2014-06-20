import pygtk
pygtk.require('2.0')
import gtk

import dialogs.download

class LeftBar(gtk.VBox):

  def __init__(self, parent):
    gtk.VBox.__init__(self, False, 0)

    self.parent_window = parent
    self.settings = parent.stuff.settings

    self.create_buttons()
    self.create_separator()
    self.create_sort_by()
    self.create_separator()
    self.create_view()
    self.create_separator()
    self.create_tags()
    self.show()

  def create_label(self, val):
    l = gtk.Label(val)
    l.set_alignment(xalign = 0.0, yalign = 0.5)
    l.show()
    self.pack_start(l, False, False, 0)

  def create_separator(self):
    sep = gtk.HSeparator()
    sep.show()
    self.pack_start(sep, False, False, 10)

  def create_view(self):
    self.create_label("View")
    d = {
      "Title": "view_title", "Subtitle": "view_subtitle", "Tags": "view_tags",
      "Filename": "view_filename", "Preview": "view_preview",
      "Progress": "view_progress"
      }
    for label, conf in d.items():
      c = gtk.CheckButton(label)
      c.connect("toggled", self.view_toggled)
      c.set_active(self.settings.vars[conf])
      c.show()
      self.pack_start(c, False, False, 0)

  def create_button(self, label, callback):
    button = gtk.Button(label)
    button.connect("clicked", callback, None)
    button.show()
    self.pack_start(button, False, False, 0)

  def create_buttons(self):
    self.create_button("Download PDF from URL", self.download_dialog)
    self.create_button("Settings", self.settings_dialog)
    self.create_button("Check for new files", self.check_new_files)

  def create_sort_by(self):
    self.create_label("Sort by")

    c = gtk.CheckButton("Filename")
    c.set_active(self.settings.vars["sort_by_filename"])
    c.show()
    self.pack_start(c, False, False, 0)

  def create_tags(self):
    l = gtk.Label("Tags")
    l.set_alignment(xalign = 0.0, yalign = 0.5)
    l.show()
    self.pack_start(l, False, False, 0)

    visible_tags = set(self.settings.vars["visible_tags"].split(","))
    self.tag_visibility = {}
    for tag in self.parent_window.tags():
      self.tag_visibility[tag] = tag in visible_tags

    self.tag_boxes = gtk.VBox(False, 0)
    for tag in sorted(self.parent_window.tags()):
      c = gtk.CheckButton(tag)
      c.show()
      c.set_active(self.tag_visibility[tag])
      c.connect("toggled", self.tag_toggled, tag)
      self.tag_boxes.pack_start(c, False, False, 0)
    self.tag_boxes.show()
    self.pack_start(self.tag_boxes, False, False, 5)



  def view_toggled(self, widget, data = None):
    l = widget.get_label()
    mapping = {"Title": "view_title", "Subtitle": "view_subtitle",
      "Tags": "view_tags", "Filename": "view_filename", "Preview": "view_preview",
      "Progress": "view_progress"}
    if l in mapping:
      self.settings.vars[mapping[l]] = widget.get_active()
      self.settings.commit()
      self.parent_window.update_items(l, widget.get_active())

  def tag_toggled(self, widget, tag = None):
    self.tag_visibility[tag] = widget.get_active()
    self.parent_window.update_table(self.tag_visibility)

  def update_tags(self):
    for i in self.tag_boxes.get_children():
      self.tag_boxes.remove(i)
    for tag in sorted(self.parent_window.tags()):
      c = gtk.CheckButton(tag)
      c.show()
      if tag in self.tag_visibility: # tag is already known
        c.set_active(self.tag_visibility[tag])
      else: # tag is new
        self.tag_visibility[tag] = True
      c.set_active(self.tag_visibility[tag])
      c.connect("toggled", self.tag_toggled, (c, tag))
      self.tag_boxes.pack_start(c, False, False, 0)


  def settings_dialog(self, widget, data = None):
    dialog = dialogs.settings.DialogSettings("Settings", None, gtk.DIALOG_MODAL, self.settings)
    dialog.show()

  def download_dialog(self, widget, data = None):
    dialog = dialogs.download.DialogDownload("Download PDF", None, gtk.DIALOG_MODAL)
    dialog.show()

  def check_new_files(self, widget, data = None):
    pdfdb = self.parent_window.stuff.pdfdb
    files = pdfdb.check_for_new_files()
    n = len(files)
    if n == 0:
      label = gtk.Label("No new files have been found.")
      dialog = gtk.Dialog("Check for new files.", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
      dialog.vbox.pack_start(label, False, False, 10)
      label.show()
      dialog.show()
      dialog.run()
      dialog.destroy()
    else:
      s = "" if n == 1 else "s"
      l1 = gtk.Label("Found " + str(n) + " new file" + s + ".")
      s = "it" if n == 1 else "them"
      l2 = gtk.Label("Do you want to import " + s + "?")
      dialog = gtk.Dialog("Check for new files.", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
      dialog.vbox.pack_start(l1, False, False, 10)
      l1.show()
      dialog.vbox.pack_start(l2, False, False, 10)
      l2.show()
      dialog.show()
      r = dialog.run()
      dialog.destroy()
      if r == gtk.RESPONSE_ACCEPT:
        self.import_new_files(files)

  def ignore_close_event(self, widget, event):
    return True

  def import_new_files(self, files):
    n = len(files)
    self.import_dialog = gtk.Dialog("Import files", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
    l = gtk.Label("Importing files...")
    l.set_alignment(xalign = 0.0, yalign = 0.5)
    l.show()
    self.import_dialog.vbox.pack_start(l, False, False, 0)
    self.import_p = gtk.ProgressBar()
    self.import_p.set_text("0/" + str(n))
    self.import_p.show()
    self.import_dialog.vbox.pack_start(self.import_p, True, False, 0)
    self.import_dialog.vbox.set_spacing(5)
    self.import_dialog.show()
    self.import_dialog.connect("delete-event", self.ignore_close_event)
    self.parent_window.stuff.pdfdb.import_files(files, self.update_import)

  def update_import(self, done, remaining):
    f = float(done) / (done + remaining)
    self.import_p.set_fraction(f)
    self.import_p.set_text(str(done) + "/" + str(done + remaining))
    if remaining == 0:
      self.import_dialog.destroy()
      self.import_dialog = None
      self.parent_window.update_table()

      label = gtk.Label("New files have been tagged with the tag 'new'.")
      dialog = gtk.Dialog("Importing done.", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
      dialog.vbox.pack_start(label, False, False, 10)
      label.show()
      dialog.show()
      dialog.run()
      dialog.destroy()

    while gtk.events_pending():
      gtk.main_iteration(False)
