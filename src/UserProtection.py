import winreg
import Details
import ctypes

started_up = "SU1"
passwd = 'passwd'
keywd = 'keywd'
key_path = rf"SOFTWARE\{Details.applicationName}"

def write_to_registry(name, value):
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
        print("Data written to registry key successfully.")
        winreg.CloseKey(key)
    except Exception as e:
        print("Error writing to registry:", e)


def read_from_registry(name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, name)
        print("Value read from registry key:", value)
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        print("Registry key does not exist.")
    except Exception as e:
        print("Error reading from registry:", e)


def delete_registry_value(value_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, value_name)
        print(f"Value '{value_name}' deleted successfully from registry key '{key_path}'.")
        winreg.CloseKey(key)
    except FileNotFoundError:
        print("Registry key or value does not exist.")
    except Exception as e:
        print("Error deleting registry value:", e)


def check_registry_value(value_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        value, value_type = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        if value:
            return True
        return False
    except FileNotFoundError:
        print("Registry key or value does not exist.")
        return False
    except Exception as e:
        print("Error accessing registry value:", e)
        return False


def lock_screen():
    user32 = ctypes.windll.LoadLibrary("user32.dll")
    user32.LockWorkStation()
