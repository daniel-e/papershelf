import os, sys, re, sys
import settings

def child(pdffile):
  f = open("/dev/null", "w")
  os.dup2(sys.stdout.fileno(), f.fileno())
  os.dup2(sys.stderr.fileno(), f.fileno())
  s = settings.Settings()
  os.execvp(s.vars["pdfviewer"], [s.vars["pdfviewer"], pdffile])
  sys.exit(1)

def short_name(n):
  n = n.lower().replace(' ', '_')
  n = re.sub('-', '_', n)
  n = re.sub('\'', '', n)
  n = re.sub(':', '', n)
  n = re.sub('^._', '', n)
  n = re.sub('^.._', '', n)
  n = re.sub('^..._', '', n)
  n = re.sub('_._', '_', n)
  n = re.sub('_.._', '_', n)
  n = re.sub('_..._', '_', n)
  while len(n) > 30:
    p = n.rfind("_")
    n = n[:p]
  return n

def next_number():
  s = settings.Settings()
  path = s.vars["pdflocation"]
  max = 0
  files = [f for f in os.listdir(path) if os.path.isfile(path + "/" + f)]
  for f in files:
    c = re.compile('^([0-9]+)_.*')
    m = c.match(f)
    if m:
      if int(m.group(1)) > max: max = int(m.group(1))
  return max + 1

def download_pdf(url):
  f = tempfile.NamedTemporaryFile(delete = False, suffix = ".getpdf.pdf")
  pdf = urllib2.urlopen(self.url.get_text()).read()
  f.write(pdf)
  f.close()
  return f.name

def extern_pdf_view(fname):
  pid = os.fork()
  if pid == 0:
    child(fname)
    sys.exit(1)
