import win32con
import win32api
import ctypes
import os
import stat
from pathlib import Path

def hide_file(filename):
    win32api.SetFileAttributes(filename,win32con.FILE_ATTRIBUTE_HIDDEN)

def unhide_file(filename):
    win32api.SetFileAttributes(filename,win32con.FILE_ATTRIBUTE_NORMAL)

def hide_dir(dir):
    ctypes.windll.kernel32.SetFileAttributesW(dir, win32con.FILE_ATTRIBUTE_HIDDEN)

def unhide_dir(dir):
    ctypes.windll.kernel32.SetFileAttributesW(dir, win32con.FILE_ATTRIBUTE_NORMAL)

def is_file_hidden(dest):
    return bool(os.stat(dest).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)


def is_dir_hidden(dest):
    if bool(os.stat(dest).st_file_attributes & 2):
        return True
