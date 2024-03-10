import win32con
import win32api
import ctypes


def hide_file(filename):
    win32api.SetFileAttributes(filename,win32con.FILE_ATTRIBUTE_HIDDEN)

def unhide_file(filename):
    win32api.SetFileAttributes(filename,win32con.FILE_ATTRIBUTE_NORMAL)

def hide_dir(dir):
    ctypes.windll.kernel32.SetFileAttributesW(dir, win32con.FILE_ATTRIBUTE_HIDDEN)

def unhide_dir(dir):
    ctypes.windll.kernel32.SetFileAttributesW(dir, win32con.FILE_ATTRIBUTE_NORMAL)
