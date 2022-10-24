import re
import time

txt = "hello hello {={ param }=} hello"
rep = r"{={(.*)}=}"
param = "+++HHHHH+++"

print(re.sub(rep, param, txt))

time.sleep(30)
