import winreg
from winreg import QueryValueEx, EnumKey
import logging


def print_lists(lst):
    for k, elm in enumerate(lst):
        logging.info("{}: {}".format(k + 1, elm[0]))


class RegistryConnection:
    def __init__(self):
        self.registry_cursor = None
        self.dir_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        self.hkey_dict = {winreg.HKEY_LOCAL_MACHINE: 'HKEY_LOCAL_MACHINE',
                          winreg.HKEY_CURRENT_USER: 'HKEY_CURRENT_USER'}

    def connect_to_main_key(self, key):
        self.registry_cursor = winreg.ConnectRegistry(None, key)

    def open_element_by_key(self, mainKey, key):
        try:
            return winreg.OpenKey(mainKey, key)
        except EnvironmentError:
            logging.info("***cursor is empty ***")

    def get_software_data_by_field(self, software_key, requested_data_field):
        return QueryValueEx(software_key, requested_data_field)

    def get_software_enum_key(self, directory_conn, software_index):
        return EnumKey(directory_conn, software_index)


if __name__ == "__main__":
    log_name = 'log_file'
    logging.basicConfig(filename=log_name,
                        filemode='a',
                        format='%(asctime)s %(message)s',
                        level=logging.INFO)
    requested_data_field = "DisplayName"  # choose here which field you need
    reg_conn = RegistryConnection()
    software_lst = []
    for hkey in reg_conn.hkey_dict:
        reg_conn.connect_to_main_key(hkey)  # establish connection to registry
        dir_conn = reg_conn.open_element_by_key(reg_conn.registry_cursor,
                                                reg_conn.dir_path)  # establish connection to registry dir
        for i in range(1024):
            try:
                software_key = reg_conn.get_software_enum_key(dir_conn, i)
                software_conn = reg_conn.open_element_by_key(dir_conn,
                                                             software_key)  # establish connection to software file
                val = reg_conn.get_software_data_by_field(software_conn, requested_data_field)
                software_lst.append(val)
            except FileNotFoundError:
                continue
            except EnvironmentError:
                logging.info(r"*** %s files was found in %s ***" % (i, reg_conn.hkey_dict[hkey]))
                break
    print_lists(software_lst)
