import winreg
from winreg import QueryValueEx, EnumKey

key_dict = {winreg.HKEY_LOCAL_MACHINE: 'HKEY_LOCAL_MACHINE', winreg.HKEY_CURRENT_USER: 'HKEY_CURRENT_USER'}

def connect_to_registry(key):
    reg = winreg.ConnectRegistry(None, key)
    return reg


def get_sw_lst_key(reg_conn):
    k = winreg.OpenKeyEx(reg_conn, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
    return k


def get_sw_lst(aRegHK):
    aKey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    aReg = connect_to_registry(aRegHK)
    print(r"*** Reading from %s %s ***" % (key_dict[aRegHK], aKey))
    aKey = winreg.OpenKey(aReg, aKey)
    requested_data_field = "DisplayName"  # choose here which field you need
    sw_lst = []
    for i in range(1024):
        try:
            asubkey_name = EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            val = QueryValueEx(asubkey, requested_data_field)
            sw_lst.append(val)
            print(val)
        except FileNotFoundError:
            continue
        except EnvironmentError:
            print(r"*** %s files was found ***" % i)
            break
    return sw_lst


if __name__ == "__main__":
    aRHK = winreg.HKEY_LOCAL_MACHINE
    l_lm = get_sw_lst(aRHK)
    aRHK = winreg.HKEY_CURRENT_USER
    l_cu = get_sw_lst(aRHK)
