import os, tempfile, sqlite3, sys, thread

import images, pdf
from pdfdb_item import Item

class PDFdb():

  def __init__(self, settings):
    self.settings = settings
    self.init_db()
    self.read_db()

  def read_db(self):
    self.paper_items = []
    self.tags = {}
    rows = self.db_query("SELECT fname, fid, tags, notes, authors, abstract, year, title, subtitle, progress from data WHERE 1=1")
    for r in rows:
      item = Item(self, self.settings)
      item.fname = str(r[0])
      item.fid = r[1]
      item.tags = r[2]
      item.set_notes("" if not r[3] else str(r[3]))
      item.set_authors("" if not r[4] else str(r[4]))
      item.set_abstract("" if not r[5] else str(r[5]))
      item.set_year(r[6])
      item.set_title("" if not r[7] else str(r[7]))
      item.set_subtitle("" if not r[8] else str(r[8]))
      item.set_progress(r[9])
      self.paper_items.append(item)
    self.update_tags()

  def update_item(self, item):
    con = sqlite3.connect(self.settings.vars["pdfdb"])
    c = con.cursor()

    fname = buffer(item.filename())
    tags = ",".join(item.get_tags())
    notes = buffer(item.get_notes())
    authors = buffer(item.get_authors())
    abstract = buffer(item.get_abstract())
    year = item.get_year()
    title = buffer(item.get_title())
    fid = item.id()
    subtitle = buffer(item.get_subtitle())
    progress = item.get_progress()

    s = "UPDATE data SET fname=?,tags=?,notes=?,authors=?,abstract=?,year=?,title=?,subtitle=?,progress=? WHERE fid=?"
    c.execute(s, (fname, tags, notes, authors, abstract, year, title, subtitle, progress, fid))
    con.commit()
    con.close()

  def rename(self, item, new_fname):
    p = self.settings.vars["pdflocation"]
    if os.path.exists(p + "/" + new_fname):
      return False
    try:
      os.rename(p + "/" + item.filename(), p + "/" + new_fname)
      item.set_filename(new_fname)
      self.update_item(item)
      return True
    except:
      return False

  def update_tags(self):
    self.tags = {}
    for i in self.paper_items:
      self.add_tags(i.get_tags(), i.id())

  def get_tags(self):
    return self.tags.keys()

  def add_tags(self, tags, fid):
    if not tags:
      return
    for tag in tags:
      if tag not in self.tags:
        self.tags[tag] = []
      self.tags[tag].append(fid)

  def update_tag(self, item):
    con = sqlite3.connect(self.settings.vars["pdfdb"])
    c = con.cursor()
    tags = ",".join(item.get_tags())
    s = "UPDATE data SET tags=? WHERE fid=?"
    c.execute(s, (tags, item.id()))
    con.commit()
    con.close()
    self.update_tags()

  def update_notes(self, item, notes):
    try:
      item.set_notes(notes)
      con = sqlite3.connect(self.settings.vars["pdfdb"])
      c = con.cursor()
      s = "UPDATE data SET notes=? WHERE fid=?"
      c.execute(s, (buffer(notes), item.id()))
      con.commit()
      con.close()
      return True
    except:
      return False

  def init_db(self):
    con = sqlite3.connect(self.settings.vars["pdfdb"])
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS preview (fid integer, img blob)''')
    cols = ["fid integer primary key autoincrement",
            "fname text",
            "tags text",
            "notes text", "authors text", "abstract text", "year text",
            "title text", "subtitle text", "progress integer"]
    c.execute("CREATE TABLE IF NOT EXISTS data (" + ",".join(cols) + ")")
    con.commit()
    con.close()

  def db_query(self, query):
    con = sqlite3.connect(self.settings.vars["pdfdb"])
    c = con.cursor()
    c.execute(query)
    r = c.fetchall()
    con.close()
    return r

  def items(self):
    return self.paper_items

  def check_for_new_files(self):
    path = self.settings.vars["pdflocation"]
    fnames = set(i.filename() for i in self.items())
    newfiles = []
    for p in os.listdir(path):
      if p not in fnames:
        newfiles.append(p)
    return newfiles

  def delete(self, item):
    con = sqlite3.connect(self.settings.vars["pdfdb"])
    c = con.cursor()
    c.execute("DELETE FROM preview WHERE fid=?", [item.id()])
    c.execute("DELETE FROM data WHERE fid=?", [item.id()])
    con.commit()
    con.close()
    try:
      os.unlink(self.settings.vars["pdflocation"] + "/" + item.filename())
    except:
      pass
    del self.paper_items[item.id()]

  def update_preview(self, item, filename):
    conv = self.settings.vars["pdfconvert"]
    path = self.settings.vars["pdflocation"]
    fname = pdf.create_preview(conv, filename)
    if images.image_height(fname) > 181:
      images.resize_height(fname, 140, 181)
    f = open(fname, "rb")
    data = f.read()
    f.close()
    os.unlink(fname)

    con = sqlite3.connect(self.settings.vars["pdfdb"])
    c = con.cursor()
    c.execute("UPDATE preview SET img=? WHERE fid=?", [buffer(data), item.id()])
    con.commit()
    con.close()

    item.update_preview()

  def import_file(self, filename):
    conv = self.settings.vars["pdfconvert"]
    path = self.settings.vars["pdflocation"]
    fname = pdf.create_preview(conv, path + "/" + filename)
    if images.image_height(fname) > 181:
      images.resize_height(fname, 140, 181)
    f = open(fname, "rb")
    data = f.read()
    f.close()
    os.unlink(fname)

    con = sqlite3.connect(self.settings.vars["pdfdb"])
    c = con.cursor()
    c.execute("INSERT INTO data (fname, tags) VALUES (?, 'new')", [buffer(filename)])
    fid = c.lastrowid
    c.execute("INSERT INTO preview (fid, img) VALUES (?, ?)", [fid, buffer(data)])
    con.commit()
    con.close()
    self.read_db()

  def import_files(self, files, callback):
    callback(0, len(files))
    for n, f in enumerate(files, 1):
      print "importing file", f, "..."
      self.import_file(f)
      callback(n, len(files) - n)
