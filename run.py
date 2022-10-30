import re
import yaml
import os
#import difflib
from yaml.loader import SafeLoader


class IAC_MNG:

    #parm
    rep = r"{={(.*)}=}"
    #
    param = "+++HHHHH+++"
    path = ""
    path_tmp = ""

    #template file
    def parser(self):

        #add config
        cf = self.conf()
        print(cf)
        self.path = cf #cf["pr_folder"][0]
        self.path_tmp = self.path+"tmp/"

        #Проверка папки tmp
        self.cope_tmp()

        with open(self.path+'vars.yaml') as f:
            vars = yaml.load(f, Loader=SafeLoader)
            #print(vars["vars"].items())
            #print(list(vars["vars"].items())[0])

        i = 0
        while i < len(vars["file"]):
            #parm
            rep2 = r".*/"
            rpl = ""
            fl = re.sub(rep2, rpl, self.path+vars["file"][i])

            print("")
            print("\033[37;1;41m !!! \033[0m",fl,"\033[37;1;41m !!! \033[0m")
            print("\033[37;1;41m ==================================================================================================================================== \033[0m")

            file = open(self.path+vars["file"][i])
            txt = file.read()
            file.close()


            y = 0
            while y < len(vars["vars"]):
                param = list(vars["vars"].items())[y][1]
                rep = r"{={(\s*"+list(vars["vars"].items())[y][0]+"\s*)}=}"
                txt = re.sub(rep, param, txt)
                y = y + 1


            with open(self.path_tmp+fl, "w") as f:
                f.write(txt)


            print(txt)
            print("\033[37;1;41m ==================================================================================================================================== \033[0m")

            i = i + 1
        #Run ansible-playbook main.yaml
        os.system("cd "+self.path_tmp+" && ansible-playbook main.yaml")

    #Проверка существоания папки tmp
    def cope_tmp(self):
        if os.path.exists(self.path_tmp):
            print("==>",self.path_tmp)
            os.system("cp -r "+self.path+"templates/ansible/* "+self.path_tmp)
            print("cp -r "+self.path+"templates/ansible/* "+self.path_tmp)

            os.system("cp -r "+self.path+"templates/terraform/* "+self.path_tmp)
            print("cp -r "+self.path+"templates/terraform/* "+self.path_tmp)

            os.system("cp -r "+self.path+"templates/docker_compose/* "+self.path_tmp)
            print("cp -r "+self.path+"templates/docker_compose/* "+self.path_tmp)
        else:
            print('Объект не найден')
            os.system("rm -rf "+self.path_tmp)
            print("rm -rf "+self.path_tmp)

            os.system("mkdir "+self.path_tmp)
            print("mkdir "+self.path_tmp)

            os.system("cp -r "+self.path+"templates/ansible/* "+self.path_tmp)
            print("cp -r "+self.path+"templates/ansible/* "+self.path_tmp)

            os.system("cp -r "+self.path+"templates/terraform/* "+self.path_tmp)
            print("cp -r "+self.path+"templates/terraform/* "+self.path_tmp)

            os.system("cp -r "+self.path+"templates/docker_compose/* "+self.path_tmp)
            print("cp -r "+self.path+"templates/docker_compose/* "+self.path_tmp)

    #Add config
    def conf(self):
        if os.path.exists("conf.yaml"):
            with open('conf.yaml') as f:
                conf = yaml.load(f, Loader=SafeLoader)
            print("\033[37;1;41m ==================================================================================================================================== \033[0m")
            i = 0 
            while i < len(conf['pr_folder']):
                print(i+1," | ",conf['pr_folder'][i])
                i = i + 1
            inp = input("==>:")
            return conf['pr_folder'][int(inp)-1]
        else:
            os.system("echo '#config' > conf.yaml")


a = IAC_MNG()
a.parser()
