'''
Description: Editor's info in the top of the file
Author: p1ay8y3ar
Date: 2021-02-17 14:28:31
LastEditor: p1ay8y3ar
LastEditTime: 2021-02-17 16:27:41
Email: p1ay8y3ar@gmail.com
'''


import  winreg as wg
from JavaEnvSwitcher.src.exefile.key_config import ENV_PATH,jdk_path,Oracle_PATH,JSON_PATH
import re
import os
import json
import time
import  ctypes
class Switcher:
    def __init__(self):
        pass

    def open_key_handle(self,path):
        try:
            return wg.OpenKey(wg.HKEY_LOCAL_MACHINE, path)
        except:
            return  None
    def close_key(self,hkey):
        wg.CloseKey(hkey)

    def __sys_env_handle(self):
        '''
        get system path key handle ,use it private
        :return:  handle of the system path reg
        '''
        try:
            key_handle = wg.OpenKey(wg.HKEY_LOCAL_MACHINE,
                                  ENV_PATH, 0, wg.KEY_ALL_ACCESS)
            return key_handle

        except Exception as e:
            print(e)
            return None

    def sys_jdkenv_path(self):
        '''

        :return: system jdk path
        '''
        try:
            '''
            get all system path variable
            '''
            self.sys_handle = self.__sys_env_handle()
            if self.sys_handle==None: return ""

            query_result = wg.QueryValueEx(self.sys_handle, 'path')

            self.envint=query_result[1]
            env_str=query_result[0]

            self.envstrlist=env_str.split(";")
            self.__weekout_invalid_path(self.envstrlist)
            '''
            get jdk version
            '''
            pattern=r"\\jdk-*[\d+-.\w]*\\bin"
            for i in range(len(self.envstrlist)):

                if self.envstrlist[i]==Oracle_PATH:
                    '''剔除旧版jdk的的path'''
                    self.envstrlist.pop(i)
                    continue
                re_match=re.search(pattern,self.envstrlist[i])
                if re_match==None:
                    continue
                else:
                    self.nowenv=self.envstrlist.pop(i)
                    return self.nowenv
            return ""
        except PermissionError:
            return "None"
        except Exception as e:
            print(e)
            return "None"

    def java_install_path(self):
        '''
        get java_install_path in windows
        :return: a tuple ,which contains list of java install paths
        '''
        self.jdk_list=[]
        for path in jdk_path:

            jdk_handle = self.open_key_handle(path)
            if jdk_handle==None:continue
            sub_keycount = wg.QueryInfoKey(jdk_handle)[0]  # 显示子键的数量
            for i in range(sub_keycount):
                sub_key = path + "\\" + wg.EnumKey(jdk_handle, i)
                sub_handle = self.open_key_handle(sub_key)
                if sub_handle==None:continue
                sub_str = wg.QueryValueEx(sub_handle, 'JavaHome')
                self.jdk_list.append(sub_str[0])

        custom_path =self.loadpath_fromjson()
        self.jdk_list.extend(custom_path)
        return set(self.jdk_list)
    def __weekout_invalid_path(self,pathlist):
        for i in range(len(pathlist)):
            if pathlist[i].strip()=="":
                pathlist.pop(i)
    def path_check(self,path)->bool:
        bin_path="\\bin"
        java_path="\\bin\\java.exe"
        lib_path="\\lib"
        try:
            if not os.path.exists(path):return False
            if not os.path.exists(path+lib_path):return False
            if not os.path.exists(path+bin_path):return False
            if not os.path.exists(path+java_path):return False
        except:
            return False
        return True

    def savato_json(self,localpath):
        try:

            if os.path.exists(JSON_PATH):
                with  open(JSON_PATH, "a+")as f:
                    loaded =json.load(f)
                    path_dict =loaded["localpath"]
                    for k,v in path_dict.items():
                        if localpath==v:
                            return True
                    loaded["localpath"][int(time.time())] = localpath
                    json.dump(loaded, f)
            else:
                with  open(JSON_PATH, "a+")as f:
                    loaded = {}
                    loaded["localpath"] = {}
                    loaded["localpath"][int(time.time())] = localpath
                    json.dump(loaded,f)
                    return True
        except Exception as e:
            print(e)
            return False

    def loadpath_fromjson(self)->list:
        return_list=[]
        try:

            if os.path.exists(JSON_PATH):

                with  open(JSON_PATH, "r")as f:
                    loaded =json.load(f)
                    path_dict =loaded["localpath"]
                    for k,v in path_dict.items():
                        return_list.append(v)
            return return_list
        except:
            os.remove(JSON_PATH)
            return return_list

    def set_new_env(self,path):
        '''
        set env now
        :param path:
        :return:
        '''
        try:
            #路径检测
            print(path)
            if not self.path_check(path):return False
            if path not in self.jdk_list:

                self.savato_json(path)
                self.jdk_list.append(path)

            orgin_path=";".join(self.envstrlist)
            new_path=path+"\\bin"+';'+orgin_path
            wg.SetValueEx(self.sys_handle, 'path', '', self.envint, new_path)
            new_CLASSPATH=".;"+path+"\\lib"
            wg.SetValueEx(self.sys_handle, 'CLASSPATH', '', self.envint, new_CLASSPATH)
            wg.SetValueEx(self.sys_handle, 'JAVA_HOME', '', self.envint, path)
            wg.FlushKey(self.sys_handle)
            self.__broadcast()

            return True
        except:
            return False

    def __del__(self):
        if self.sys_handle!=None and self.sys_handle!="":

            self.close_key(self.sys_handle)

    def __broadcast(self):

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_long()
        SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
        SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u"Environment", SMTO_ABORTIFHUNG, 5000,
                            ctypes.byref(result), )