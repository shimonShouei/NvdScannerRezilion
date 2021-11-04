import winreg
from winreg import QueryValueEx, EnumKey

key_dict = {winreg.HKEY_LOCAL_MACHINE: 'HKEY_LOCAL_MACHINE', winreg.HKEY_CURRENT_USER: 'HKEY_CURRENT_USER'}

def connect_to_registry(key):
    reg = winreg.ConnectRegistry(None, key)
    return reg

def get_software_lst(MainKey):
    aKey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    aReg = connect_to_registry(MainKey)
    print(r"*** Reading from %s %s ***" % (key_dict[MainKey], aKey))
    aKey = winreg.OpenKey(aReg, aKey)
    requested_data_field = "DisplayName"  # choose here which field you need
    software_lst = []
    for i in range(1024):
        try:
            asubkey_name = EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            val = QueryValueEx(asubkey, requested_data_field)
            software_lst.append(val)
            print(val[0])
        except FileNotFoundError:
            continue
        except EnvironmentError:
            print(r"*** %s files was found ***" % i)
            break
    return software_lst


if __name__ == "__main__":
    LocalMachList = get_software_lst(winreg.HKEY_LOCAL_MACHINE)
    CurUserList = get_software_lst(winreg.HKEY_CURRENT_USER)
