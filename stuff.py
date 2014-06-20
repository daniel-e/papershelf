import settings
import pdf_db

class Stuff:

  def __init__(self):
    self.settings = settings.Settings()
    self.pdfdb = pdf_db.PDFdb(self.settings)
