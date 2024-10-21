import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import os
import time
import ctypes

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("File Manager")
        self.iconbitmap("icon.ico")
        self.minsize(width=800,height=600)
        self.maxsize(width=800,height=600)
        self.configure(padx=20,pady=20)

        self.folder_path = None
        self.selected_path_index = None
        self.selected_path_value = None
        self.create_item_name = None
        self.path_list = list()

        self.open_folder_button = tk.Button(self,text="Open folder",command=self.open_folder,padx=6,pady=4)
        self.open_folder_button.place(relx=0,rely=0)

        self.open_item_button = tk.Button(self, text="Clear", command=self.clear_listbox,padx=6,pady=4)
        self.open_item_button.place(relx=0.115, rely=0)

        self.open_item_button = tk.Button(self, text="Open", command=self.open_new_folder,padx=6,pady=4)
        self.open_item_button.place(relx=0.18, rely=0)

        self.delete_item_button = tk.Button(self, text="Delete", command=self.delete_item,padx=6,pady=4)
        self.delete_item_button.place(relx=0.248, rely=0)

        self.create_folder_button = tk.Button(self, text="Create Folder", command=self.create_folder, padx=6, pady=4)
        self.create_folder_button.place(relx=0.321, rely=0)

        self.create_file_button = tk.Button(self, text="Create File", command=self.create_file, padx=6, pady=4)
        self.create_file_button.place(relx=0.445, rely=0)

        self.path_listbox = tk.Listbox(self,width=90,height=25)
        self.path_listbox.place(relx=0, rely=0.1)

        self.path_info_listbox = tk.Listbox(self,width=35,height=25)
        self.path_info_listbox.place(relx=0.72,rely=0.1)


        self.path_listbox.bind("<<ListboxSelect>>",self.info_path)
        self.path_listbox.bind("<Double-Button-1>", self.start_item)

        """
        self.file_listbox.bind("<Button-3>", self.close_new_file)
        self.in_file_listbox.bind("<<ListboxSelect>>",lambda for_warning: print(for_warning))"""

        self.github_link = tk.Label(self,text="github.com/mustafaicer")
        self.github_link.place(relx=0.5,rely=0.95,anchor=tk.CENTER)

    def get_selected_path(self):
        try:
            self.selected_path_index = self.path_listbox.curselection()
            self.selected_path_value = self.path_listbox.get(self.selected_path_index)
        except:
            pass

    def open_folder(self):
        try:
            self.folder_path = filedialog.askdirectory()
            for name in os.listdir(self.folder_path):
                path = os.path.join(self.folder_path, name)
                self.path_list.append(path)
            self.path_list.append(self.folder_path)
            for path in self.path_list:
                self.path_listbox.insert(0,path)
        except Exception as error:
            messagebox.showerror("Error open folder",f"{error}")

    def refresh_listbox(self):
        try:
            self.path_listbox.delete(0, tk.END)
            for path in self.path_list:
                self.path_listbox.insert(0, path)
        except Exception as error:
            messagebox.showerror("Error refresh listbox",f"{error}")

    def clear_listbox(self):
        try:
            self.folder_path = None
            self.selected_path_index = None
            self.selected_path_value = None
            self.path_list.clear()
            self.path_listbox.delete(0, tk.END)
            self.path_info_listbox.delete(0, tk.END)
        except Exception as error:
            messagebox.showerror("Error clear listbox", f"{error}")

    def open_new_folder(self):
        self.get_selected_path()
        try:
            for new_item_name in os.listdir(self.selected_path_value):
                new_item_path = os.path.join(self.selected_path_value, new_item_name)
                self.path_list.append(new_item_path)
            self.refresh_listbox()
        except Exception as error:
            messagebox.showerror("Error open new folder",f"{error}")

    def delete_item(self):
        try:
            self.get_selected_path()
            response = ask_delete(f"Are you sure for delete {self.selected_path_value}")
            if response == 6:
                try:
                    os.remove(self.selected_path_value)
                except:
                    os.rmdir(self.selected_path_value)
                self.path_list.remove(self.selected_path_value)
                self.refresh_listbox()
            else:
                pass
        except Exception as error:
            messagebox.showerror("Error delete item", f"{error}")

    def create_folder(self):
        self.get_selected_path()
        try:
            take_folder_name = simpledialog.askstring("Create Folder","Enter folder name : ")
            created_folder_path = None
            if take_folder_name is not None:
                try:
                    created_folder_path = os.path.join(self.selected_path_value, take_folder_name)
                    os.mkdir(created_folder_path)
                except:
                    created_folder_path = os.path.join(self.folder_path, take_folder_name)
                    os.mkdir(created_folder_path)
                self.path_list.append(created_folder_path)
                self.refresh_listbox()
        except Exception as error:
            messagebox.showerror("Error create folder",f"{error}")

    def create_file(self):
        self.get_selected_path()
        try:
            take_file_name = simpledialog.askstring("Create File","Enter file name : ")
            created_folder_path = None
            if take_file_name is not None:
                try:
                    try:
                        created_folder_path = os.path.join(self.selected_path_value, take_file_name)
                        with open(created_folder_path, "w") as file:
                            file.write(" ")
                    except:
                        created_folder_path = os.path.join(self.folder_path, take_file_name)
                        with open(created_folder_path, "w") as file:
                            file.write(" ")
                    self.path_list.append(created_folder_path)
                except Exception as error:
                    messagebox.showerror("Error creating file",f"{error}")
            self.refresh_listbox()
        except Exception as error:
            messagebox.showerror("Error create file",f"{error}")

    def info_path(self,for_warning):
        try:
            self.get_selected_path()
            size_of_file = os.path.getsize(self.selected_path_value)
            create_date_of_file = time.ctime(os.path.getctime(self.selected_path_value))
            change_date_of_file = time.ctime(os.path.getmtime(self.selected_path_value))

            info_list = [
                f"Change date : {change_date_of_file}",
                f"Create date : {create_date_of_file}",
                f"Size : {size_of_file} bytes"
            ]

            self.path_info_listbox.delete(0,tk.END)
            for info in info_list:
                self.path_info_listbox.insert(0,info)

        except Exception as error:
            messagebox.showerror("Error info path",f"{error}")

    def start_item(self,for_warning):
        try:
            self.get_selected_path()
            os.startfile(self.selected_path_value)
        except Exception as error:
            messagebox.showerror("Error start item", f"{error}")

def ask_delete(message):
    return ctypes.windll.user32.MessageBoxW(0,message,"Delete?",4)

if __name__ == "__main__":
    window = App()
    window.mainloop()