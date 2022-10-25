import re
import yaml
import os
from yaml.loader import SafeLoader

#parm
rep = r"{={(.*)}=}"
#
param = "+++HHHHH+++"

path = "project/"
path_tmp = path+"tmp/"

#template file
def parser():
    os.system("rm -rf "+path_tmp)
    print("rm -rf "+path_tmp)

    os.system("mkdir "+path_tmp)
    print("mkdir "+path_tmp)

    os.system("cp -r "+path+"templates/ansible/* "+path_tmp)
    print("cp -r "+path+"templates/ansible/* "+path_tmp)

    os.system("cp -r "+path+"templates/terraform/* "+path_tmp)
    print("cp -r "+path+"templates/terraform/* "+path_tmp)

    with open(path+'vars.yaml') as f:
        vars = yaml.load(f, Loader=SafeLoader)
        #print(vars["vars"].items())
        #print(list(vars["vars"].items())[0])

    i = 0
    while i < len(vars["file"]):
        print("")
        print(vars["file"][i])
        print("====================================================================================================================================")

        file = open(path+vars["file"][i])
        txt = file.read()
        file.close()


        y = 0
        while y < len(vars["vars"]):
            param = list(vars["vars"].items())[y][1]
            rep = r"{={(\s*"+list(vars["vars"].items())[y][0]+"\s*)}=}"
            txt = re.sub(rep, param, txt)
            y = y + 1

        #parm
        rep2 = r".*/"
        rpl = ""
        fl = re.sub(rep2, rpl, path+vars["file"][i])

        with open(path_tmp+fl, "w") as f:
            f.write(txt)

        print(txt)
        print("====================================================================================================================================")
        i = i + 1


# def import_playbook():
#     with open(path+'vars.yaml') as f:
#         vars = yaml.load(f, Loader=SafeLoader)
#         #print(vars["vars"].items())
        
#     #vars = vars["import_playbook"]
#     i = 0
#     while i < len(vars["import_playbook"]):
#         file = open(path+vars["import_playbook"][i])
#         txt = file.read()
#         file.close()


#         with open(path_tmp+fl, "w") as f:
#             f.write(txt)


#         print(txt)
#         i = i + 1

parser()
