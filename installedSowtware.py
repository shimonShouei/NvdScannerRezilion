import winreg
from winreg import QueryValueEx

reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
k = winreg.OpenKeyEx(reg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{090DCBF9-8353-4E9D-B155-337B2A324D1B}')
val = QueryValueEx(k, "DisplayName")
print(val)