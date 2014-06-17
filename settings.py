import os, shelve

class Settings:

  def __init__(self):
    self.home = os.path.expanduser("~") + "/.papershelf/"
    if not os.path.exists(self.home):
      os.mkdir(self.home)
    if not os.path.exists(self.home + "pdf"):
      os.mkdir(self.home + "pdf")
    if not os.path.exists(self.home + "settings"):
      self.init_default(True)
    else:
      self.load_settings()

  def init_default(self, commit):
    d = {}
    d["pdfviewer"] = "/usr/bin/evince"
    d["pdflocation"] = self.home + "pdf/"
    d["pdfconvert"] = "/usr/bin/convert"
    d["pdfdb"] = self.home + "db"
    d["sort_by_filename"] = True
    d["view_filename"] = True
    d["view_preview"] = True
    d["view_title"] = True
    d["view_subtitle"] = True
    d["view_tags"] = True
    d["windowwidth"] = 800
    d["windowheight"] = 900
    d["vpos"] = 0
    self.vars = d
    if commit:
      self.commit()

  def load_settings(self):
    self.init_default(False)
    d = shelve.open(self.home + "settings")
    for k, v in d.items():
      self.vars[k] = v
    d.close()

  def commit(self):
    d = shelve.open(self.home + "settings")
    for k, v in self.vars.items():
      d[k] = v
    d.close()
