import pygtk
pygtk.require('2.0')
import gtk
import shutil, urllib2, os, tempfile

import dialogs.tags
import tools, settings, dialog_correct, dialog_settings, dialog_download
import dialog_notes, dialog_details, dialog_rename, dialog_progress
import left_bar
import pdf_db, tools

class MainWindow:

  def run(self):
    gtk.main()

  def __init__(self):
    self.pdfdb = pdf_db.PDFdb()
    self.settings = settings.Settings()
    self.WIDTH = self.settings.vars["windowwidth"]
    self.HEIGHT = self.settings.vars["windowheight"]
    self.items = {}
    self.tagdata = None

    self.init_window()

  def tags(self):
    return self.pdfdb.get_tags()

  def set_image(self, i, item):
    buf = gtk.gdk.PixbufLoader()
    buf.write(item.get_preview())
    buf.close()
    i.set_from_pixbuf(buf.get_pixbuf())

  def create_item(self, item):
    v = gtk.VBox(False, 0)
    v.show()

    # -----
    l = gtk.Label(item.short_filename())
    l.show()

    # -----
    i = gtk.Image()
    self.set_image(i, item)
    i.show()

    # -----
    tags = gtk.Label(", ".join(item.get_tags()))
    tags.show()

    # -----
    prgr = gtk.HBox(False, 0)
    prgr.show()
    p = gtk.ProgressBar()
    p.show()
    p.set_text(str(item.get_progress()) + "%")
    p.set_fraction(float(item.get_progress()) / 100.0)
    p.set_usize(120, -1)
    # hack to center the progressbar
    ll = gtk.Label("")
    ll.show()
    prgr.pack_start(ll, expand = True)
    prgr.pack_start(p, expand = False)
    ll = gtk.Label("")
    ll.show()
    prgr.pack_start(ll, expand = True)

    # -----
    vb = gtk.VBox(False, 0)
    vb.show()
    for k in tools.wrap_string(item.get_title()):
      t = gtk.Label("<b>" + k + "</b>")
      t.set_justify(gtk.JUSTIFY_CENTER)
      # http://faq.pygtk.org/index.py?req=show&file=faq07.003.htp
      t.set_use_markup(True)
      t.show()
      vb.pack_start(t, False, False, 2)

    # -----
    vbs = gtk.VBox(False, 0)
    vbs.show()
    for k in tools.wrap_string(item.get_subtitle()):
      t = gtk.Label(k)
      t.set_justify(gtk.JUSTIFY_CENTER)
      t.show()
      vbs.pack_start(t, False, False, 2)

    # -----
    if not self.settings.vars["view_preview"]:
      i.hide()
    v.pack_start(i, False, False, 5)
    if not self.settings.vars["view_title"]:
      vb.hide()
    v.pack_start(vb, False, False, 0)
    if not self.settings.vars["view_subtitle"]:
      vbs.hide()
    v.pack_start(vbs, False, False, 0)
    if not self.settings.vars["view_progress"]:
      prgr.hide()
    v.pack_start(prgr, False, False, 5)
    if not self.settings.vars["view_filename"]:
      l.hide()
    v.pack_start(l, False, False, 5)
    if not self.settings.vars["view_tags"]:
      tags.hide()
    v.pack_start(tags, False, False, 0)

    # -----
    e = gtk.EventBox()
    e.add(v)
    e.show()
    e.add_events(gtk.gdk.BUTTON_PRESS_MASK)
    e.connect("button_press_event", self.viewpdf, item)

    d = {"filename": l, "image": i, "tags": tags, "title": vb, "box": e,
      "subtitle": vbs, "progress": p}
    self.items[item.id()] = d

    return e

  def viewpdf(self, widget, event, item):
    if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
      self.context_menu(event, item)
    else:
      tools.extern_pdf_view(item.path())

  def context_menu(self, event, item):
    menu = gtk.Menu()

    menu_item = gtk.MenuItem("Tags")
    menu_item.connect("activate", self.manage_tags, item)
    menu.append(menu_item)
    menu_item.show()

    menu_item = gtk.MenuItem("Notes")
    menu_item.connect("activate", self.notes, item)
    menu.append(menu_item)
    menu_item.show()

    menu_item = gtk.MenuItem("Details")
    menu_item.connect("activate", self.details, item)
    menu.append(menu_item)
    menu_item.show()

    menu_item = gtk.MenuItem("Set progress")
    menu_item.connect("activate", self.progress, item)
    menu.append(menu_item)
    menu_item.show()

    menu_item = gtk.MenuItem("Rename file")
    menu_item.connect("activate", self.rename_file, item)
    menu.append(menu_item)
    menu_item.show()

    menu_item = gtk.MenuItem("Delete file")
    menu_item.connect("activate", self.remove_file, item)
    menu.append(menu_item)
    menu_item.show()

    menu_item = gtk.MenuItem("Replace cover")
    menu_item.connect("activate", self.replace_cover, item)
    menu.append(menu_item)
    menu_item.show()

    menu.popup(None, None, None, event.button, event.time, None)
    menu.show_all()

  def progress(self, widget, item):
    dialog = dialog_progress.DialogProgress("Set progress", None, gtk.DIALOG_MODAL, item)
    dialog.show()
    if dialog.run() == 1: # Ok
      p = dialog.get_progress()
      item.set_progress(p)
      self.pdfdb.update_item(item)
      self.items[item.id()]["progress"].set_fraction(float(p) / 100.0)
      self.items[item.id()]["progress"].set_text(str(p) + "%")
    dialog.destroy()


  def replace_cover(self, widget, item):
    f = gtk.FileChooserDialog("Select an image", None,
      buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    if f.run() == gtk.RESPONSE_OK:
      self.pdfdb.update_preview(item, f.get_filename())
      d = self.items[item.id()]
      i = d["image"]
      self.set_image(i, item)
    f.destroy()

  def rename_file(self, widget, item):
    dialog = dialog_rename.DialogRename("Rename file", None, gtk.DIALOG_MODAL, item)
    dialog.show()
    if dialog.run() == 1: # Ok
      if not self.pdfdb.rename(item, dialog.get_new_filename()):
        dialogerr = gtk.Dialog("Error", None, gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        l = gtk.Label("An error occured. Could not rename file.")
        l.show()
        dialogerr.vbox.pack_start(l)
        dialogerr.show()
        dialogerr.run()
        dialogerr.destroy()
      else:
        data = self.items[item.id()]
        l = data["filename"]
        l.set_text(item.short_filename())
    dialog.destroy()

  def remove_file(self, widget, item):
    dg = gtk.Dialog("Delete file", None, gtk.DIALOG_MODAL,
      (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
    l = gtk.Label("Do you really want to delete the file?")
    l.show()
    dg.vbox.pack_start(l)
    dg.show()
    if dg.run() == gtk.RESPONSE_ACCEPT:
      self.pdfdb.delete(item)
    dg.destroy()
    self.update_table()

  def details(self, widget, item):
    dialog = dialog_details.DialogDetails("Details", None, gtk.DIALOG_MODAL, item, self)
    dialog.show()
    r = dialog.run()
    if r == 1: # Ok
      item.set_abstract(dialog.get_abstract())
      item.set_title(dialog.get_title())
      item.set_year(dialog.get_year())
      item.set_authors(dialog.get_authors())
      item.set_subtitle(dialog.get_subtitle())
      self.pdfdb.update_item(item)
      # update view
      d = self.items[item.id()]
      #d["title"].set_text(item.get_title())
      #d["subtitle"].set_text(item.get_subtitle())
    dialog.destroy()

  def manage_tags(self, widget, item = None):
    dialog = dialogs.tags.DialogTags("Edit tags", None, gtk.DIALOG_MODAL, item, self.pdfdb.get_tags())
    dialog.show()
    r = dialog.run()
    tags = dialog.get_tags() # list of tags, lower cased, stripped
    dialog.destroy()
    if r == 1: # update button
      self.update_tags(tags, item)

  def notes(self, widget, item):
    dialog = dialog_notes.DialogNotes("Notes", None, gtk.DIALOG_MODAL, item, self)
    dialog.show()
    dialog.run()
    dialog.destroy()

  # tags = list of tags, lower cased, stripped
  def update_tags(self, tags, item):
      item.set_tags(tags)
      self.pdfdb.update_tag(item)
      tag_visibility = self.left_bar.update_tags()
      self.update_table(tag_visibility)

  def fill_table(self, t, tag_visibility = None):
    items = self.pdfdb.items()
    if self.settings.vars["sort_by_filename"]:
      items = sorted(items, key = lambda i: i.filename())

    if tag_visibility:
      k = []
      for item in items:
        for tag in item.get_tags():
          if tag in tag_visibility and tag_visibility[tag]:
            k.append(item)
            break
      items = k

    n = len(items)
    cols = 3
    rows = int( n / cols)
    if n % cols != 0:
      rows += 1
    t.resize(max(rows, 1), cols)
    for i, item in enumerate(items):
      y = int(i / cols)
      x = i % cols
      t.attach(self.create_item(item), x, x + 1, y, y + 1, xoptions = gtk.EXPAND)

    self.tagdata = tag_visibility

  def update_table(self, tag_visibility = None):
    for i in self.table.get_children():
      self.table.remove(i)
    t = tag_visibility
    if not t:
      t = self.tagdata
    self.fill_table(self.table, t)

  def update_items(self, what, state):
    # what = Title|Tags|Filename|Preview|Subtitle|Progress
    # filename, image, tags, title, subtitle, progress
    mapping = {"Title": "title", "Tags": "tags", "Filename": "filename",
      "Preview": "image", "Subtitle": "subtitle", "Progress": "progress"}
    for k, v in self.items.items():
      if state:
        v[mapping[what]].show()
      else:
        v[mapping[what]].hide()

  def init_window(self):
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title("PaperShelf")
    self.window.set_border_width(10)
    self.window.connect("destroy", self.destroy)
    self.window.set_position(gtk.WIN_POS_CENTER)

    #m = gtk.Menu()
    #m.show()

    tags = self.settings.vars["visible_tags"]
    t = {}
    for i in tags.split(","):
      t[i] = True

    self.table = gtk.Table(rows = 1, columns = 1, homogeneous = True)
    self.table.set_col_spacings(10)
    self.table.show()
    self.fill_table(self.table, t)

    self.sc = gtk.ScrolledWindow()
    self.sc.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
    self.sc.show()
    self.sc.add_with_viewport(self.table)

    # left bar
    self.left_bar = left_bar.LeftBar(self)

    h = gtk.HBox(False, 0)
    h.pack_start(self.left_bar, False, False, 0)
    sep = gtk.VSeparator()
    sep.show()
    h.pack_start(sep, False, False, 10)
    h.pack_start(self.sc, True, True, 0)
    h.show()

    self.window.resize(self.WIDTH, self.HEIGHT)
    self.window.add(h)
    self.window.show()

    self.sc.get_vadjustment().set_value(self.settings.vars["vpos"])

  def destroy(self, widget, data = None):
    # adjustment of vertical scrollbar
    self.settings.vars["vpos"] = self.sc.get_vadjustment().get_value()
    # save tags on exit
    visible_tags = []
    for i in self.left_bar.tag_boxes.get_children():
      if i.get_active():
        visible_tags.append(i.get_label())
    self.settings.vars["visible_tags"] = ",".join(visible_tags)
    self.settings.commit()
    gtk.main_quit()
