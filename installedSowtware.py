import winreg
from winreg import QueryValueEx, EnumKey


def connect_to_registry(key):
    reg = winreg.ConnectRegistry(None, key)
    return reg


def get_sw_lst_key(reg_conn):
    k = winreg.OpenKeyEx(reg_conn, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
    return k


def get_sw_lst(aReg):
    aKey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    print(r"*** Reading from %s ***" % aKey)
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
    aR = connect_to_registry(winreg.HKEY_LOCAL_MACHINE)
    l = get_sw_lst(aR)
