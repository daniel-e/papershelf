import os, tempfile, sqlite3, sys, thread

import images, settings, pdf

class Item():

  def __init__(self, parent, settings):
    self.s = settings
    self.preview = None
    self.parent = parent
    self.notes = ""

  def filename(self):
    return self.fname

  def path(self):
    return self.s.vars["pdflocation"] + "/" + self.filename()

  def id(self):
    return self.fid

  def short_filename(self):
    if len(self.fname) > 23:
      return self.fname[0:20] + "..."
    return self.fname

  def get_preview(self):
    if not self.preview:
      r = self.parent.db_query("SELECT img FROM preview WHERE fid=%d" % self.id())
      if len(r) > 0:
        self.preview = str(r[0][0])
    if not self.preview:
      f = open("noimage.jpg")
      self.preview = f.read()
      f.close()
    return self.preview

  def get_tags(self):
    return [i.strip() for i in self.tags.split(",")]

  def set_tags(self, tags):
    self.tags = ",".join(tags)

  def get_notes(self):
    return self.notes

  def set_notes(self, notes):
    self.notes = ""
    if notes:
      self.notes = notes

  def set_authors(self, authors):
    self.authors = authors

  def get_authors(self):
    return self.no_none(self.authors)

  def set_abstract(self, abstract):
    self.abstract = abstract

  def get_abstract(self):
    return self.no_none(self.abstract)

  def set_year(self, year):
    self.year = year

  def get_year(self):
    return self.no_none(self.year)

  def set_title(self, title):
    self.title = title

  def get_title(self):
    return self.no_none(self.title)

  def no_none(self, str):
    if str:
      return str
    return ""


class PDFdb():

  def __init__(self):
    self.s = settings.Settings()
    self.init_db()
    self.read_db()
    #self.update_db()
    #self.create_previews()

  def read_db(self):
    self.paper_items = []
    self.tags = {}
    rows = self.db_query("SELECT fname, fid, tags, notes, authors, abstract, year, title from data WHERE 1=1")
    for r in rows:
      item = Item(self, self.s)
      item.fname = str(r[0])
      item.fid = r[1]
      item.tags = r[2]
      item.set_notes("" if not r[3] else str(r[3]))
      item.set_authors("" if not r[4] else str(r[4]))
      item.set_abstract("" if not r[5] else str(r[5]))
      item.set_year(r[6])
      item.set_title("" if not r[7] else str(r[7]))
      self.paper_items.append(item)
    self.update_tags()

  def update_item(self, item):
    con = sqlite3.connect(self.s.vars["pdfdb"])
    c = con.cursor()

    fname = buffer(item.filename())
    tags = ",".join(item.get_tags())
    notes = buffer(item.get_notes())
    authors = buffer(item.get_authors())
    abstract = buffer(item.get_abstract())
    year = item.get_year()
    title = buffer(item.get_title())
    fid = item.id()

    s = "UPDATE data SET fname=?,tags=?,notes=?,authors=?,abstract=?,year=?,title=? WHERE fid=?"
    c.execute(s, (fname, tags, notes, authors, abstract, year, title, fid))
    con.commit()
    con.close()


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
    con = sqlite3.connect(self.s.vars["pdfdb"])
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
      con = sqlite3.connect(self.s.vars["pdfdb"])
      c = con.cursor()
      s = "UPDATE data SET notes=? WHERE fid=?"
      c.execute(s, (buffer(notes), item.id()))
      con.commit()
      con.close()
      return True
    except:
      return False

  def init_db(self):
    con = sqlite3.connect(self.s.vars["pdfdb"])
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS preview (fid integer, img blob)''')
    cols = ["fid integer primary key autoincrement",
            "fname text",
            "tags text",
            "notes text", "authors text", "abstract text", "year text"]
    c.execute("CREATE TABLE IF NOT EXISTS data (" + ",".join(cols) + ")")
    con.commit()
    con.close()

  def db_query(self, query):
    con = sqlite3.connect(self.s.vars["pdfdb"])
    c = con.cursor()
    c.execute(query)
    r = c.fetchall()
    con.close()
    return r

  def items(self):
    return self.paper_items

  def check_for_new_files(self):
    path = self.s.vars["pdflocation"]
    fnames = set(i.filename() for i in self.items())
    newfiles = []
    for p in os.listdir(path):
      if p not in fnames:
        newfiles.append(p)
    return newfiles

  def import_file(self, filename):
    conv = self.s.vars["pdfconvert"]
    path = self.s.vars["pdflocation"]
    fname = pdf.create_preview(conv, path + "/" + filename)
    if images.image_height(fname) > 181:
      images.resize_height(fname, 140, 181)
    f = open(fname, "rb")
    data = f.read()
    f.close()
    os.unlink(fname)

    con = sqlite3.connect(self.s.vars["pdfdb"])
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
