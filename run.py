import re
import time

#file
#txt = "hello hello {={ param }=} hello"
#parm
rep = r"{={(.*)}=}"
#
param = "+++HHHHH+++"

#print(re.sub(rep, param, txt))

#template file

def parser():
    file = open("project/templates/terraform/main.tf")
    txt = file.read()
    print(re.sub(rep, param, txt))
    file.close()

#time.sleep(30)
parser()