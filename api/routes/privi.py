import os
import stat

def isgroupreadable(filepath):
  st = os.stat(filepath)

  print(stat.filemode(st.st_mode)) 



isgroupreadable("/root/mercado/api/borrar.txt.2")