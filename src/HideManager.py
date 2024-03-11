import win32con
import win32api
import ctypes
import os
import stat
from pathlib import Path
from ProtectionEngine import encryptionExtension

def hide_file(filename):
    try:
        win32api.SetFileAttributes(filename,win32con.FILE_ATTRIBUTE_HIDDEN)
    except Exception as f:
        print("Error when hidding file, ", f)

def unhide_file(filename):
    try:
        win32api.SetFileAttributes(filename,win32con.FILE_ATTRIBUTE_NORMAL)
    except Exception as f:
        print("Error when unhidding file, ", f)

def hide_dir(dir):
    try:
        ctypes.windll.kernel32.SetFileAttributesW(dir, win32con.FILE_ATTRIBUTE_HIDDEN)
    except Exception as f:
        print("Error when hidding dir, ", f)

def unhide_dir(dir):
    try:
        ctypes.windll.kernel32.SetFileAttributesW(dir, win32con.FILE_ATTRIBUTE_NORMAL)
    except Exception as f:
        print("Error when unhidding dir, ", f)

def is_file_hidden(dest):
    return bool(os.stat(dest).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def is_dir_hidden(dest):
    if bool(os.stat(dest).st_file_attributes & 2):
        return True

def has_secured_files(dest):
    has_hidden = False
    for i in os.listdir(dest):
        if i.endswith(encryptionExtension):
            has_hidden = True
            break
    return has_hidden
