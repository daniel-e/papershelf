from PIL import Image

def image_height(fname):
  im = Image.open(fname)
  w, h = im.size
  return h

def resize_height(fname, width, height):
  im = Image.open(fname)
  size = width, height
  im.thumbnail(size, Image.ANTIALIAS)
  im.save(fname, "jpeg")
