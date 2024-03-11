import os.path
import time
import win32api
from ctk_components import *
from tkinter import StringVar
from PIL import Image
from CTkToolTip import CTkToolTip
from CTkMessagebox import CTkMessagebox
from shutil import copytree, rmtree
import threading
from KeyGen import generate_keys
from EncryptPassword import *
from ProtectionEngine import scanRecurse, encrypt, decrypt, encryptionExtension
from pathlib import Path
from HideManager import hide_file, hide_dir, unhide_file, unhide_dir, is_file_hidden, is_dir_hidden, has_secured_files


class SecureExplorer:

    ctk.set_appearance_mode("dark")
    widthIconsLength = 7
    lastWidthIconsLength = 0
    absPath = r""
    lastAbsPath = r""
    buttonPressed = ""
    buttonPresses = 0
    lastButtonObj = None
    badopitons = ["$RECYCLE.BIN", "$Recycle.Bin", "System Volume Information", "desktop.ini"]
    iconsPath = "icons/"
    folder_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "open-folder.png"), dark_image=Image.open(iconsPath + "open-folder.png"), size=(50, 50))
    secure_folder_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "secure-open-folder.png"), dark_image=Image.open(iconsPath + "secure-open-folder.png"), size=(50, 50))
    small_folder_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "open-folder.png"), dark_image=Image.open(iconsPath + "open-folder.png"), size=(15, 15))
    disk_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "harddisk.png"), dark_image=Image.open(iconsPath + "harddisk.png"), size=(80, 80))
    file_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "file.png"), dark_image=Image.open(iconsPath + "file.png"), size=(50, 50))
    secure_file_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "secure-file.png"), dark_image=Image.open(iconsPath + "secure-file.png"), size=(50, 50))
    small_file_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "file.png"), dark_image=Image.open(iconsPath + "file.png"), size=(15, 15))
    copy_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "copy.png"), dark_image=Image.open(iconsPath + "copy.png"), size=(20, 20))
    paste_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "paste.png"), dark_image=Image.open(iconsPath + "paste.png"), size=(20, 20))
    rename_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "rename.png"), dark_image=Image.open(iconsPath + "rename.png"), size=(20, 20))
    delete_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "delete.png"), dark_image=Image.open(iconsPath + "delete.png"), size=(20, 20))
    creatnew_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "new.png"), dark_image=Image.open(iconsPath + "new.png"), size=(20, 20))
    left_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "left.png"), dark_image=Image.open(iconsPath + "left.png"), size=(25, 25))
    right_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "right.png"), dark_image=Image.open(iconsPath + "right.png"), size=(25, 25))
    home_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "home.png"), dark_image=Image.open(iconsPath + "home.png"), size=(25, 25))
    lock_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "lock.png"), dark_image=Image.open(iconsPath + "lock.png"), size=(25, 32))
    unlock_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "unlock.png"), dark_image=Image.open(iconsPath + "unlock.png"), size=(25, 32))
    logout_icon = ctk.CTkImage(light_image=Image.open(iconsPath + "logout.png"), dark_image=Image.open(iconsPath + "logout.png"), size=(25, 25))
    currentItems = []
    isCopy = False
    copyitem = None
    copydata = None

    def detect_window_resizing(self):
        while 1:
            try:
                time.sleep(0.1)
                self.top.update()
                if self.top.winfo_width() > 1600:
                    self.widthIconsLength = int(str(self.top.winfo_width())[:-2])-2
                else:
                    self.widthIconsLength = int(str(self.top.winfo_width())[:-2])-1
                if self.widthIconsLength != self.lastWidthIconsLength:
                    self.lastWidthIconsLength = self.widthIconsLength
                    if self.absPath == r"":
                        pass
                    else:
                        self.re_align_window()
                else:
                    pass
            except:
                pass

    def creat_new(self):
        if self.absPath == r"" :
            CTkMessagebox(self.top, title="Error!", message=f"Can't create new item here!!", icon="cancel")
        else:
            if CTkMessagebox(self.top, title="Warning!", message=f"What do you want to create new?", option_1="File", option_2="Folder", icon="question").get() == "Folder":
                foldername = ctk.CTkInputDialog(title="Required", text="Type a name for new folder").get_input()
                if os.path.exists(self.absPath + foldername):
                    CTkMessagebox(self.top, title="Error!", message=f"Folder with name '{foldername}' already exists!", icon="cancel")
                else:
                    os.mkdir(self.absPath + foldername)
            else:
                filename = ctk.CTkInputDialog(title="Required", text="Type a name for new file").get_input()
                if os.path.exists(self.absPath + filename):
                    CTkMessagebox(self.top, title="Error!", message=f"File with name '{filename}' already exists!", icon="cancel")
                else:
                    open(self.absPath + filename, 'w').write("")
            self.layerSearch(self.absPath)

    def rename(self, _):
        item = self.remove_newline(_)
        itempath = self.absPath + _
        if item in self.listDisks():
            CTkMessagebox(self.top, title="Fatal error!", message=f"Can't rename disk '{item}' or any other disks!!", icon="cancel")
        else:
            newname = ctk.CTkInputDialog(title="Required", text="Type a new name you want to change to").get_input()
            if os.path.exists(self.absPath + newname):
                CTkMessagebox(self.top, title="Error!", message=f"Name '{newname}' already exists!", icon="cancel")
            else:
                os.rename(itempath, self.absPath + newname)
            self.layerSearch(self.absPath)

    def copy(self, _):
        self.copyitem = self.absPath + self.remove_newline(_)
        if self.copyitem in self.listDisks():
            CTkMessagebox(self.top, title="Fatal error!", message=f"Can't copy disk '{self.copyitem}' or any other disks!!", icon="cancel")
        else:
            self.isCopy = True
            if os.path.isdir(self.copyitem):
                self.copydata = self.copyitem
            else:
                self.copydata = open(self.copyitem, "rb").read()
            self.selected(self.remove_newline(_) + " - copy", iscopy=True)
            self.paste_button.configure(state="normal")

    def paste(self):
        item = self.copyitem.split("\\")[-1]
        self.itempath = self.absPath + item

        if self.isCopy:
            if os.path.exists(self.itempath):
                i = 1
                while 1:
                    new_item_name = self.itempath + " (" + str(i) + ")"
                    if not os.path.exists(new_item_name):
                        self.itempath = new_item_name
                        break

            self.paste_button.configure(state="disabled")
            if os.path.isdir(self.copyitem):
                new_dir = self.absPath + self.copyitem.split("\\")[-1]
                os.mkdir(new_dir)
                copytree(self.copydata, new_dir)
            else:
                open(self.itempath, "wb").write(self.copydata)
            self.layerSearch(self.absPath)

    def delete(self, _):
        item = self.remove_newline(_)
        itempath = self.absPath + item
        if item in self.listDisks():
            CTkMessagebox(self.top, title="Fatal error!", message=f"Can't delete any disk !!", icon="cancel")
        else:
            try:
                if CTkMessagebox(self.top, title="Warning!", message=f"You will delete '{item}'\nAre you sure!!", option_1="Ok!", option_2="Cancel", icon="cancel").get() == "Ok!":
                    if os.path.isdir(itempath):
                        try:
                            rmtree(itempath)
                        except OSError:
                            CTkMessagebox(self.top, title="Access error!", message=f"Can't delete, maybe folder is not empty!", icon="cancel")
                    else:
                        os.remove(itempath)
                    self.layerSearch(self.absPath)
                    self.reset_selected()
            except PermissionError:
                CTkMessagebox(self.top, title="Access error!", message=f"Access is denied", icon="cancel")

    def listDisks(self):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        return drives

    def clear_window(self):
        for _ in self.currentItems:
            _.grid_forget()
        self.currentItems = []

    def re_align_window(self):
        columsNO = 0
        rowNO = 0
        for _ in self.currentItems:
            _.grid(row=rowNO, column=columsNO, padx=6, pady=5, sticky="n")
            columsNO += 1
            if columsNO >= self.widthIconsLength:
                columsNO = 0
                rowNO += 1

    def remove_newline(self, text):
        if "\n" in text:
            text = text.replace("\n", "")
        return text

    def calc_abs_path(self, current):
        self.lastAbsPath = self.absPath
        if self.absPath == r"":
            self.absPath += self.remove_newline(current)
        else:
            self.absPath += self.remove_newline(current) + "\\"
        return self.absPath

    def return_forward(self, *args):
        if self.lastAbsPath == r"" or self.absPath == r"" or self.lastAbsPath == self.absPath or len(self.absPath) > len(self.lastAbsPath):
            pass
        else:
            self.clear_window()
            self.layerSearch(self.lastAbsPath, forward=True)
            self.display_path(self.lastAbsPath)
            forward = self.lastAbsPath.split("\\")
            for _ in forward:
                if _ == "":
                    forward.pop(forward.index(_))
            self.calc_abs_path(forward[-1])
            self.reset_selected()

    def return_back(self, *args):
        if self.absPath == r"":
            pass
        else:
            self.clear_window()
            self.lastAbsPath = self.absPath
            back = self.absPath.split("\\")
            self.absPath = r""
            for _ in back:
                if _ == "":
                    back.pop(back.index(_))
            if len(back) > 1:
                for _ in back[:-1]:
                    self.absPath += _ + "\\"
                self.layerSearch(self.absPath)
                self.display_path(self.absPath)
            else:
                self.home_menu()
            self.reset_selected()

    def home_menu(self):
        self.absPath = r""
        self.clear_window()
        for disk in self.listDisks():
            self.new_button(disk, row=0, column=self.listDisks().index(disk), image=self.disk_icon)
        self.display_path("Home")
        self.reset_selected()

    def layerSearch(self, dest, forward=False):
        columsNO = 0
        rowNO = 0
        try:
            newItems = os.listdir(dest)
            self.clear_window()
            gotoPath = self.absPath
            if forward:
                gotoPath = self.lastAbsPath
            for dir in range(0, len(newItems)):
                if newItems[dir] in self.badopitons:
                    continue
                if os.path.isfile(gotoPath + newItems[dir]) or os.path.isfile(gotoPath + newItems[dir]):
                    if is_file_hidden(gotoPath + newItems[dir]) and newItems[dir].endswith(encryptionExtension):
                        self.new_button(destination=newItems[dir], row=rowNO, column=columsNO, image=self.secure_file_icon)
                    else:
                        self.new_button(destination=newItems[dir], row=rowNO, column=columsNO, image=self.file_icon)
                else:
                    if is_dir_hidden(gotoPath + newItems[dir]) and has_secured_files(gotoPath + newItems[dir]):
                        self.new_button(destination=newItems[dir], row=rowNO, column=columsNO, image=self.secure_folder_icon)
                    else:
                        self.new_button(destination=newItems[dir], row=rowNO, column=columsNO, image=self.folder_icon)
                columsNO += 1
                if columsNO >= self.widthIconsLength:
                    columsNO = 0
                    rowNO += 1
            self.display_path(gotoPath)
        except PermissionError:
            CTkMessagebox(self.top, title="Access error!", message=f"Access is denied", icon="cancel")
            self.return_back()

    def display_path(self, path):
        self.pathString.set(value="")
        self.pathString.set(value=path)

    def selected(self, item, iscopy=False):
        if "\n" in item:
            item = self.remove_newline(item)
        if iscopy:
            item = item.replace(" - copy", "")
            nitem = " " + self.remove_newline(item) + " - copy"
        else:
            nitem = item
        if os.path.isdir(self.absPath + self.remove_newline(item)):
            self.selected_label.configure(text=nitem, image=self.small_folder_icon)
        else:
            self.selected_label.configure(text=nitem, image=self.small_file_icon)

    def reset_selected(self):
        if not self.isCopy:
            try:
                self.selected_label.destroy()
            except:
                pass
            self.selected_label = ctk.CTkLabel(self.top, text="", width=785, height=20, fg_color=self.top.cget("fg_color"), font=("roboto", 14), compound="left")
            self.selected_label.grid(row=1, column=0, pady=2)
            self.buttonPressed = ""

    def entry_search(self, *args):
        try:
            if not self.path_entry.get() == "":
                self.absPath = self.path_entry.get()
                self.layerSearch(self.path_entry.get())
        except:
            CTkMessagebox(self.top, title="Path error", message="Wrong path or invalid syntax!", icon="cancel")

    def secure(self, dest):
        if any(dest == i for i in self.listDisks()):
            CTkMessagebox(title="Action error!", message="Select a file or folder to secure it.", icon="cancel")
            return -1
        destination = self.absPath + dest

        with open(Details.publicKeyPath, 'rb') as f:
            pubKey = f.read()

        if os.path.isdir(destination):
            for item in scanRecurse(destination):
                filePath = Path(item)
                if str(filePath).endswith(encryptionExtension):
                    continue
                reply = encrypt(filePath, pubKey)
                hide_dir(destination)
                if reply == -1:
                    CTkMessagebox(title="File type error!", message="Unsupported supported file type!", icon="cancel")
                    return -1
            # Refresh GUI
            self.layerSearch(self.absPath)
            self.selected_label.configure(text="", image=self.small_folder_icon)
            print("Directory Locked")
        else:
            if dest.endswith(encryptionExtension):
                CTkMessagebox(title="Action error!", message="File is already secured!", icon="cancel")
                return -1
            if '.' not in dest:
                CTkMessagebox(title="File type error!", message="Unsupported supported file type!", icon="cancel")
                return -1
            filePath = Path(destination)
            reply = encrypt(filePath, pubKey)
            hide_file(destination.split(".")[0] + encryptionExtension)
            # Refresh GUI
            self.layerSearch(self.absPath)
            self.selected_label.configure(text="", image=self.small_folder_icon)
            print("File Locked")
    
    def unlock(self, dest):
        if any(dest == i for i in self.listDisks()):
            CTkMessagebox(title="Action error!", message="Select a secured file or folder to unsecure it.", icon="cancel")
            return -1

        destination = self.absPath + dest
        with open(Details.privateKeyPath, 'rb') as f:
            privateKey = f.read()

        if os.path.isdir(destination):
            if not has_secured_files(destination):
                CTkMessagebox(title="Denied action!", message="The folder haven't secured files!", icon="cancel")
                return -1
            for item in scanRecurse(destination):
                unhide_dir(destination)
                filePath = Path(item)
                if str(filePath).endswith(encryptionExtension):
                    decrypt(filePath, privateKey)
            # Refresh GUI
            self.layerSearch(self.absPath)
            self.selected_label.configure(text="", image=self.small_folder_icon)
            print("Directory Unlocked")
        else:
            if not destination.endswith(encryptionExtension):
                CTkMessagebox(title="File type error!", message="File is not valid to unsecure", icon="cancel")
                return -1
            unhide_file(destination.split(".")[0] + encryptionExtension)
            filePath = Path(destination)
            decrypt(destination, privateKey)
            # Refresh GUI
            self.layerSearch(self.absPath)
            self.selected_label.configure(text="", image=self.small_folder_icon)
            print("File Unlocked")



    def Browser(self):
        self.top = ctk.CTk()
        self.top.minsize(width=800, height=600)
        self.top.title("Secure Explorer")
        self.top.bind("<Alt-Left>", self.return_back)
        self.top.bind("<Alt-Right>", self.return_forward)
        self.top.bind("<Delete>", lambda e:self.delete(self.buttonPressed))
        self.top.bind("<F2>", lambda e:self.rename(self.buttonPressed))
        self.top.bind("<Control-c>", lambda e:self.copy(self.buttonPressed))
        self.top.bind("<Control-v>", self.paste)

        self.ubber_left_tools_frame = ctk.CTkFrame(self.top, height=30, fg_color=self.top.cget("fg_color"))
        self.ubber_left_tools_frame.grid(row=0, column=0, sticky="w", pady=5)

        self.logout_button = ctk.CTkButton(self.ubber_left_tools_frame, text="", fg_color=self.ubber_left_tools_frame.cget("fg_color"),
                                         image=self.logout_icon, width=10, corner_radius=25, command=lambda: (self.top.destroy(), self.Login()))
        self.logout_button.pack(side="left", anchor="w")
        CTkToolTip(self.logout_button, message="Logout")
        self.home_button = ctk.CTkButton(self.ubber_left_tools_frame, text="", fg_color=self.ubber_left_tools_frame.cget("fg_color"),
                                         image=self.home_icon, width=10, corner_radius=25, command=self.home_menu)
        self.home_button.pack(side="left", anchor="w")
        CTkToolTip(self.home_button, message="Home")
        self.back_button = ctk.CTkButton(self.ubber_left_tools_frame, text="", fg_color=self.ubber_left_tools_frame.cget("fg_color"),
                                         image=self.left_icon, width=10, corner_radius=25, command=self.return_back)
        self.back_button.pack(side="left", anchor="w")
        CTkToolTip(self.back_button, message="Back")
        self.lastview_button = ctk.CTkButton(self.ubber_left_tools_frame, text="", fg_color=self.ubber_left_tools_frame.cget("fg_color"),
                                             image=self.right_icon, width=10, corner_radius=25, command=self.return_forward)
        self.lastview_button.pack(side="left", anchor="w")
        CTkToolTip(self.lastview_button, message="Last opened page")

        self.ubber_right_tools_frame = ctk.CTkFrame(self.top, height=30, fg_color=self.top.cget("fg_color"))
        self.ubber_right_tools_frame.grid(row=0, column=0, sticky="e", pady=5)

        self.createnew_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.creatnew_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                              width=20, corner_radius=25, command=self.creat_new)
        self.createnew_button.pack(side="right", anchor="e")
        CTkToolTip(self.createnew_button, message="Create new file/folder")
        self.copy_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.copy_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                         width=20, corner_radius=25, command=lambda:self.copy(self.buttonPressed))
        self.copy_button.pack(side="right", anchor="e")
        CTkToolTip(self.copy_button, message="Copy")
        self.paste_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.paste_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                          width=20, corner_radius=25, state="disabled", command=self.paste)
        self.paste_button.pack(side="right", anchor="e")
        CTkToolTip(self.paste_button, message="Paste")
        self.rename_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.rename_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                           width=20, corner_radius=25, command=lambda:self.rename(self.buttonPressed))
        self.rename_button.pack(side="right", anchor="e")
        CTkToolTip(self.rename_button, message="Rename")
        self.delete_button = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.delete_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                           width=20, corner_radius=25, command=lambda:self.delete(self.buttonPressed))
        self.delete_button.pack(side="right", anchor="e")
        CTkToolTip(self.delete_button, message="Delete")

        self.lock_data = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.lock_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                           width=20, corner_radius=25, command= lambda: self.secure(self.selected_label.cget("text")))
        self.lock_data.pack(side="right", anchor="e")
        CTkToolTip(self.lock_data, message="Secure")

        self.un_lock_data = ctk.CTkButton(self.ubber_right_tools_frame, text="", image=self.unlock_icon, fg_color=self.ubber_right_tools_frame.cget("fg_color"),
                                       width=20, corner_radius=25, command= lambda: self.unlock(self.selected_label.cget("text")))
        self.un_lock_data.pack(side="right", anchor="e")
        CTkToolTip(self.un_lock_data, message="Unsecure")

        self.selected_label = ctk.CTkLabel(self.top, text="", width=785, height=20, fg_color=self.top.cget("fg_color"), font=("roboto", 14), compound="left")
        self.selected_label.grid(row=1, column=0, pady=2)

        self.finder_frame = ctk.CTkScrollableFrame(self.top, width=770, height=500, corner_radius=0)
        self.finder_frame.grid(row=2, column=0, sticky="nsew")


        self.pathString = StringVar(value="Home")
        self.path_entry = ctk.CTkEntry(self.top, width=785, height=20, fg_color=self.finder_frame.cget("fg_color"), font=("roboto", 14), textvariable=self.pathString, border_width=0)
        self.path_entry.grid(row=3, column=0, sticky="nsew")
        self.path_entry.bind("<Return>", self.entry_search)

        self.home_menu()

        self.top.update()
        x_cordinate = int((self.top.winfo_screenwidth() / 2) - (self.top.winfo_width() / 2))
        y_cordinate = int((self.top.winfo_screenheight() / 2) - (self.top.winfo_height() / 2))
        self.top.geometry("{}+{}".format(x_cordinate, y_cordinate - 50))

        self.top.columnconfigure(0, weight=1)
        self.top.rowconfigure(2, weight=1)
        self.top.after(100, threading.Thread(target=self.detect_window_resizing, daemon=True).start)
        self.top.mainloop()

    def new_button(self, destination, row, column, image):
        if len(destination) > 10:
            indicator = 0
            ndest = ""
            for l in destination:
                if indicator == 10:
                    ndest += "\n" + l
                    indicator = 0
                else:
                    ndest += l
                indicator += 1
        else:
            ndest = destination
        if len(ndest) > 15:
            nName = ndest[0:14] + "..."
        else:
            nName = ndest
        if os.path.isdir(self.absPath + destination):
            item = ctk.CTkButton(self.finder_frame, text=nName, image=image, fg_color=self.finder_frame.cget("fg_color"), width=100, compound="top", corner_radius=15,
                                  command=lambda: self.button_action(item, ndest, logic="open"))
        else:
            item = ctk.CTkButton(self.finder_frame, text=nName, image=image, fg_color=self.finder_frame.cget("fg_color"), width=100, compound="top", corner_radius=15,
                                  command=lambda: self.button_action(item, ndest, logic="run"))
        item.grid(row=row, column=column, padx=6, pady=5, sticky="n")
        self.currentItems.append(item)

    def button_action(self, obj, btn, logic="open"):
        if btn != self.buttonPressed or self.buttonPresses == 0:
            try:
                if self.lastButtonObj:
                    self.lastButtonObj.configure(fg_color="#2b2b2b")
            except:
                pass
            self.lastButtonObj = obj
            self.buttonPressed = btn
            self.buttonPresses = 0
            self.buttonPresses += 1
            obj.configure(fg_color="#144871")
            self.selected(btn)
        else:
            try:
                if self.lastButtonObj:
                    self.lastButtonObj.configure(fg_color="#2b2b2b")
            except:
                pass
            self.lastButtonObj = None
            self.buttonPresses = 0
            if logic == "open":
                self.layerSearch(self.calc_abs_path(btn))
            else:
                os.startfile(self.absPath + self.remove_newline(btn))

    def do_login(self, *args):
        invalid = "False"
        if os.path.exists(Details.startUpFile):
            if init_pass_to_compare(self.password_input.get()) == get_password():
                open(Details.startUpFile, 'w').write("3ard el shazly el bambazz begneeeh")
            else:
                invalid = "True"
        else:
            if self.password_input1.get() == self.password_input2.get():
                if len(self.password_input2.get()) >= 8 and len(self.secret_keyword.get()) >= 6:
                    open(Details.startUpFile, 'w').write("3ard el shazly el bambazz begneeeh")
                    new_password(self.password_input1.get(), self.secret_keyword.get())
                else:
                    invalid = "Weak"
            else:
                invalid = "True"
        if invalid == "Weak":
            CTkMessagebox(title="Weak cridintials!", message="Type stronger password or stronger keyword!", icon="cancel")
        elif invalid == "True":
            CTkMessagebox(title="Password error!", message="A7a ya zmiily", icon="cancel")
        else:
            self.login.destroy()
            self.Browser()
    
    def reset_password(self):
        password = ctk.CTkInputDialog(title="Password requered!", text="Enter old password to confirm!")
        pwd = password.get_input()
        if pwd == "" or not pwd:
            return -1
        else:
            if hashlib.sha512(pwd.encode()).hexdigest() == get_password():
                os.remove(Details.startUpFile)
                os.remove(Details.passwordFile)
                self.login.destroy()
                self.Login()
            else:
                CTkMessagebox(title="Invalid password", message="Password is not valid try again!", icon='cancel')

    def forget_password(self):
        keyword = ctk.CTkInputDialog(title="Secret keyword requered!", text="Enter secret keyword to confirm!")
        kwd = keyword.get_input()
        if kwd == "" or not kwd:
            return -1
        else:
            if hashlib.sha512(kwd.encode()).hexdigest() == get_keyword():
                os.remove(Details.startUpFile)
                os.remove(Details.passwordFile)
                self.login.destroy()
                self.Login()
            else:
                CTkMessagebox(title="Invalid keyword", message="Keyword is not valid try again!", icon='cancel')

    def check_hidden_database(self, *args):
        if not is_dir_hidden(Details.databasePath):
            hide_dir(Details.databasePath)

    def Login(self):
        if not os.path.exists(Details.databasePath):
            os.mkdir(Details.databasePath)
            hide_dir(Details.databasePath)
            generate_keys()

        if not os.path.exists(Details.publicKeyPath) or not os.path.exists(Details.privateKeyPath):
            generate_keys()

        self.login = ctk.CTk()
        self.login.title("Login")
        if os.path.exists(Details.startUpFile):
            enter_password = ctk.CTkLabel(self.login, text="Enter password", font=("roboto", 22, "bold"))
            enter_password.pack(pady=20, padx=40)

            self.password_input = CTkInput(self.login, width=300, height=35, border_width=1)
            self.password_input.pack(pady=10, padx=10)
            self.password_input.password_input()
            self.password_input.bind("<Return>", self.do_login)

        else:
            enter_password = ctk.CTkLabel(self.login, text="Enter and confirm password", font=("roboto", 22, "bold"))
            enter_password.pack(pady=20, padx=40)

            self.password_input1 = CTkInput(self.login, width=300, height=35, border_width=1)
            self.password_input1.pack(pady=10, padx=10)
            self.password_input1.password_input()
            self.password_input1.bind("<Return>", self.do_login)

            self.password_input2 = CTkInput(self.login, width=300, height=35, border_width=1)
            self.password_input2.pack(pady=10, padx=10)
            self.password_input2.password_input()
            self.password_input2.bind("<Return>", self.do_login)

            enter_secret_keyword = ctk.CTkLabel(self.login, text="Type a secret keyword (important to remember!)", 
                                                font=("roboto", 15, "bold"), text_color="red")
            enter_secret_keyword.pack(pady=(20, 10), padx=40)

            self.secret_keyword = CTkInput(self.login, width=300, height=35, border_width=1)
            self.secret_keyword.pack(pady=10, padx=10)
            self.secret_keyword.bind("<Return>", self.do_login)

        save_btn = ctk.CTkButton(self.login, text="Login", font=("roboto", 16, "bold"), width=150, corner_radius=15, command=self.do_login)
        save_btn.pack(pady=(10, 20), padx=10)

        if os.path.exists(Details.startUpFile):
            rp_btn = ctk.CTkButton(self.login, text="Reset password", font=("roboto", 14, "underline"), width=150, corner_radius=15,
                                    fg_color=self.login.cget("fg_color"), hover_color=self.login.cget("fg_color"), text_color="white",
                                    command=self.reset_password)
            rp_btn.pack(pady=5, padx=10)
            
            fp_btn = ctk.CTkButton(self.login, text="Forget password!", font=("roboto", 14, "underline"), width=150, corner_radius=15,
                                    fg_color=self.login.cget("fg_color"), hover_color=self.login.cget("fg_color"), text_color="red",
                                    command=self.forget_password)
            fp_btn.pack(pady=(0, 10), padx=10)

        self.login.update()
        self.login.minsize(self.login.winfo_width(), self.login.winfo_height())
        x_cordinate = int((self.login.winfo_screenwidth() / 2) - (self.login.winfo_width() / 2))
        y_cordinate = int((self.login.winfo_screenheight() / 2) - (self.login.winfo_height() / 2))
        self.login.geometry("{}+{}".format(x_cordinate, y_cordinate - 50))
        self.login.bind("<Configure>", self.check_hidden_database)
        self.login.mainloop()


if __name__ == "__main__":
    wf = SecureExplorer()
    wf.Login()