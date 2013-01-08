import os

def check(path):
  return os.path.isfile(path)

def load(path):
  # check the file exists
  if check(path):
    file = open(path, 'r')

    data = file.read()

    file.close()

    return data

  else:
    return None