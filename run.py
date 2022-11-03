import re
import yaml
import os
from yaml.loader import SafeLoader
from random import randint


class IAC_MNG:

    #parm
    rep = r"{={(.*)}=}"
    #
    param = "+++HHHHH+++"
    path = ""
    path_tmp = ""
    
    #file
    ci_cd_file = "vars.yaml"
    conf_file = "conf.yaml"
    ci_cd_file_tmp = "tmp_"+ci_cd_file

    #template file
    def rendering_file(self,in_file):
        try:
            with open(in_file) as f:
                vars = yaml.load(f, Loader=SafeLoader)
                print(vars["render"]["file"])
                #print(list(vars["vars"].items())[0])

            i = 0
            while i < len(vars["render"]["file"]):
                self.rendering(vars["render"]["file"][i],vars["render"]["file"][i])
                i = i + 1
        except Exception as e:
            self.yaml_debug("rendering_file - error",1)
            self.yaml_debug(e.message)
            self.yaml_debug(e.args)

    #Add config
    def conf(self):
        if os.path.exists(self.conf_file):
            with open(self.conf_file) as f:
                conf = yaml.load(f, Loader=SafeLoader)
            print("\033[37;1;41m ==================================================================================================================================== \033[0m")
            i = 0 
            while i < len(conf['pr_folder']):
                print(i+1," | ",conf['pr_folder'][i])
                i = i + 1
            inp = input("==>:")
            #return conf['pr_folder'][int(inp)-1]
            self.path = conf['pr_folder'][int(inp)-1]
        else:
            os.system("echo '#config' > "+self.conf_file)

    #rendering file vars.yaml
    def rendering(self,in_file,out_file=""):

        with open(in_file) as f:
            vars = yaml.load(f, Loader=SafeLoader)
            print(vars["vars"].items())
            #print(list(vars["vars"].items())[0])


        rep2 = r".*/"
        rpl = ""
        fl = re.sub(rep2, rpl, in_file)
        print("")
        print("\033[37;1;41m !!! \033[0m",fl,"\033[37;1;41m !!! \033[0m")
        print("\033[37;1;41m ==================================================================================================================================== \033[0m")
        file = open(in_file)
        txt = file.read()
        file.close()
        y = 0
        while y < len(vars["vars"]):
            param = list(vars["vars"].items())[y][1]
            rep = r"{={(\s*"+list(vars["vars"].items())[y][0]+"\s*)}=}"
            txt = re.sub(rep, param, txt)
            y = y + 1
        with open(out_file, "w") as f:
            f.write(txt)
        print(txt)
        print("\033[37;1;41m ==================================================================================================================================== \033[0m")

    #printing from yaml file
    def yaml_print(self,txt,color=0):
        if color == 1:
            print("\033[37;1;41m"+str(txt)+"\033[0m") #RED
        elif color == 2:
            print("\033[37;1;32m"+str(txt)+"\033[0m") #GREEN
        elif color == 3:
            print("\033[33;1;34m"+str(txt)+"\033[0m") #GREEN
        else:
            print(str(txt))
        #Памятка, Таблица цветов и фонов
        #Цвет      код         код фона
        #black    30  40    \033[30m  \033[40m
        #red      31  41    \033[31m  \033[41m
        #green    32  42    \033[32m  \033[42m
        #yellow   33  43    \033[33m  \033[43m
        #blue     34  44    \033[34m  \033[44m
        #magenta  35  45    \033[35m  \033[45m
        #cyan     36  46    \033[36m  \033[46m
        #white    37  47    \033[37m  \033[47m

    #debug
    def yaml_debug(self,txt,color=0):
        if color == 1:
            print("\033[37;1;41m"+str(txt)+"\033[0m") #RED
        if color == 2:
            print("\033[37;1;32m"+str(txt)+"\033[0m") #GREEN
        elif color == 0:
            print(str(txt)) 

    #code processing method
    def prog(self,txt,cpm):
        if cpm == "py":
            random_number = randint(1, 1000)
            with open(self.path+"prog"+random_number+".py", "w") as f:
                f.write(txt)
        elif cpm == "bash":
            random_number = randint(1, 1000)
            with open(self.path+"prog"+random_number+".sh", "w") as f:
                f.write(txt)


    def test(self):
        with open(self.path+self.ci_cd_file) as f:
            vars = yaml.load(f, Loader=SafeLoader)
        print("===============================================================================================")
        print('print(vars)')
        print(vars)
        print("===============================================================================================")
        print('print(vars["vars"].items())')
        print(vars["vars"].items())       
        print("===============================================================================================")
        print('print(list(vars["level1.1"].items()))')
        print(list(vars["level1.1"].items()))
        print("===============================================================================================")
        print('print(list(vars["level1.2"].items())[2][1])')
        print(list(vars["level1.2"].items())[2][1])
        print("===============================================================================================")
        print('print(vars.keys())')
        print(vars.keys())
        print("===============================================================================================")
        print('print(vars["level3"].keys())')
        print(vars["level3"].keys())
        print("===============================================================================================")
        print('print(vars["render"].keys())')
        print(vars["render"].keys())
        print("===============================================================================================")
        print('print(vars["render"]["file"])')
        print(vars["render"]["file"])
        print("===============================================================================================")
        print("===============================================================================================")
        print('print(vars["level3"]["prog"]')
        print(vars["level3"]["prog"])
        print("===============================================================================================")

    #ci/cd execution sort
    def yaml_sort(self):
        sort_arr = []
        level = []
        try:
            with open(self.path+self.ci_cd_file) as f:
                vars = yaml.load(f, Loader=SafeLoader)
            #print(list(vars.keys()))
            i = 0
            while i < len(list(vars.keys())):
                if list(vars.keys())[i] == "debug":
                    sort_arr.append(list(vars.keys())[i])
                i = i + 1
            i = 0 
            while i < len(list(vars.keys())):
                if list(vars.keys())[i] == "vars":
                    sort_arr.append(list(vars.keys())[i])
                i = i + 1
            i = 0 
            while i < len(list(vars.keys())):
                if list(vars.keys())[i] == "render":
                    sort_arr.append(list(vars.keys())[i])
                i = i + 1
            i = 0 
            while i < len(list(vars.keys())):
                txt = list(vars.keys())[i]
                x = re.search("level.*", txt)
                if x:
                    res = list(vars.keys())[i].strip('level')
                    level.append(res)
                i = i + 1   
            res = sorted(level, key=lambda x: x[0])     
            i = 0
            while i < len(res):
                sort_arr.append("level"+res[i])                
                i = i + 1
            #print(sort_arr)
            return sort_arr
        except Exception as e:
            self.yaml_debug("yaml_sort - error",1)
            self.yaml_debug(e.message)
            self.yaml_debug(e.args)

    #ci/cd syntax check
    def yaml_syntax_check(self,in_file):
        srt = self.yaml_sort()
        self.yaml_debug("--------------------------------")
        self.yaml_debug("      yaml_syntax_check"         )
        self.yaml_debug("--------------------------------")

        with open(in_file) as f:
            vars = yaml.load(f, Loader=SafeLoader)
        
        #data type check
        def param_type_test(pts,pts2,typ):
            #print(type(vars[pts][pts2]))
            if type(vars[pts][pts2]) == typ:                        
                self.yaml_debug("  |==> "+pts2+" - syntax check - ok",2)
            else:
                self.yaml_debug("  |==> "+pts2+" - syntax check - error",1)

        #checking elements one by one
        def param_test(param):
            self.yaml_debug(param+":")
            i = 0
            while i < len(vars[param].keys()):
                if list(vars[param].keys())[i] == "print":
                    param_type_test(param,"print",str)
                elif list(vars[param].keys())[i] == "prog":
                    param_type_test(param,"prog",str)
                elif list(vars[param].keys())[i] == "code":
                    param_type_test(param,"code",str)
                elif list(vars[param].keys())[i] == "file":
                    param_type_test(param,"file",list)
                elif list(vars[param].keys())[i] == "mode":
                    param_type_test(param,"mode",bool)
                else:
                    self.yaml_debug(vars[param]+" syntax check - error",1)
                i = i + 1
        
        def all_param_test(prm):
            i = 0
            while i < len(prm):
                if prm[i] == "vars":
                    i = i + 1
                    continue
                param_test(prm[i])
                i = i + 1

        all_param_test(srt)



a = IAC_MNG()
a.conf()
a.test()
#a.parser()
#a.yaml_print("text",3)
a.rendering(a.path+a.ci_cd_file,a.path+"tmp_"+a.ci_cd_file)
#a.rendering_file(a.path+a.ci_cd_file_tmp)
#print(a.yaml_sort())
a.yaml_syntax_check(a.path+a.ci_cd_file_tmp)