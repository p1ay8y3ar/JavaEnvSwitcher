
import ctypes
import  sys
import  os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    print("管理员")
else:
    print("不是管理员")




class Switchter:
    def __init__(self):
        pass


import winreg as wg

key_test = wg.OpenKey(wg.HKEY_LOCAL_MACHINE,r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",0,wg.KEY_ALL_ACCESS)
path_str = wg.QueryValueEx(key_test,'path')

for i in  path_str:
    if type(i)==type("str"):
        tem=i.replace(" ", "")
        print(tem)
        everypath=tem.split(";")
        print(everypath)

# 查找java的环境
# HKEY_LOCAL_MACHINE\SOFTWARE\JavaSoft

jdk_path =r"SOFTWARE\JavaSoft\JDK"
jre_path=r"SOFTWARE\JavaSoft\Java Development Kit"

jdk_handle=wg.OpenKey(wg.HKEY_LOCAL_MACHINE, jdk_path)
sub_keycount = wg.QueryInfoKey(jdk_handle)[0]#显示子键的数量

print("--------")
print(sub_keycount)

for i in  range(sub_keycount):
    print(wg.EnumKey(jdk_handle,i))
    sub_key=jdk_path+"\\" + wg.EnumKey(jdk_handle,i)
    sub_handle = wg.OpenKey(wg.HKEY_LOCAL_MACHINE, sub_key)
    sub_str = wg.QueryValueEx(sub_handle, 'JavaHome')
    print(sub_str)