import os, tempfile

def create_preview(conv, fname):
  f = tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf.jpg")
  f.close()
  pid = os.fork()
  if pid == 0:
    # i'm the child
    os.execvp(conv, [conv, "-border", "0x0", "-bordercolor", "#ffffff",
      "-resize", "140", fname + "[0]", f.name])
    sys.exit(1)
  os.waitpid(pid, 0)
  return f.name
