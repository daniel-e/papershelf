class Item():

  def __init__(self, parent, settings):
    self.settings = settings
    self.preview = None
    self.parent = parent
    self.notes = ""

  def set_filename(self, fname):
    self.fname = fname

  # TODO getter
  def filename(self):
    return self.fname

  # TODO getter
  def path(self):
    return self.settings.vars["pdflocation"] + "/" + self.filename()

  # TODO getter
  def id(self):
    return self.fid

  # TODO getter
  def short_filename(self):
    if len(self.fname) > 23:
      return self.fname[0:20] + "..."
    return self.fname

  def update_preview(self):
    # TODO sql queries should be done in pdf_db
    r = self.parent.db_query("SELECT img FROM preview WHERE fid=%d" % self.id())
    if len(r) > 0:
      self.preview = str(r[0][0])

  def get_preview(self):
    if not self.preview:
      self.update_preview()
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

  def set_subtitle(self, subtitle):
    self.subtitle = subtitle

  def get_subtitle(self):
    return self.no_none(self.subtitle)

  def set_progress(self, p):
    self.progress = p

  def get_progress(self):
    if not self.progress:
      return 0
    return self.progress

  def no_none(self, str):
    if str:
      return str
    return ""
