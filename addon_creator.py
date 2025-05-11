from tkinter.filedialog import askdirectory
from tkinter.simpledialog import askstring
from tkinter import *
from tkinter import ttk
from pathlib import Path

top = Tk()
server = IntVar()
client = IntVar()
shared = IntVar()
addon_name_var = StringVar()
addon_path = ""
answer = ""

def build_files():
    addon_name = addon_name_var.get()
    data = ""
    search_text = "ADDON_NAME"
    server_files = ["ADDON_NAME/server/sv_ADDON_NAME_database.lua", "ADDON_NAME/server/sv_ADDON_NAME_network.lua", "ADDON_NAME/server/sv_ADDON_NAME_functions.lua", "ADDON_NAME/server/sv_ADDON_NAME_hooks.lua", "ADDON_NAME/server/sv_ADDON_NAME_meta.lua"]
    client_files = ["ADDON_NAME/client/cl_ADDON_NAME_network.lua", "ADDON_NAME/client/cl_ADDON_NAME_functions.lua", "ADDON_NAME/client/cl_ADDON_NAME_vgui.lua", "ADDON_NAME/client/cl_ADDON_NAME_hooks.lua"]
    shared_files = "ADDON_NAME/config/sh_ADDON_NAME_config.lua"
    with open("./dict/start_file", "r") as file:
        data += file.read()
    if server.get():
        with open("./dict/server_part_sv", "r") as file:
            data += file.read()
        for files in server_files:
            open(addon_path + addon_name + "/lua/" + files.replace(search_text, addon_name), 'w+')
        
    if client.get():
        with open("./dict/server_part_cl", "r") as file:
            data += file.read()
        for files in client_files:
            open(addon_path + addon_name + "/lua/" + files.replace(search_text, addon_name), 'w+')
    if shared.get():
        with open("./dict/shared_server_part", "r") as file:
            data += file.read()
        open(addon_path + addon_name + "/lua/" + shared_files.replace(search_text, addon_name), 'w+')
    if client.get():
        with open("./dict/mid_part", "r") as file:
            data += file.read()
        with open("./dict/client_part_cl", "r") as file:
            data += file.read()
        if shared.get():
            with open("./dict/client_part_sh", "r") as file:
                data += file.read()
    elif shared.get():
        with open("./dict/mid_part", "r") as file:
            data += file.read()
        if shared.get():
            with open("./dict/client_part_sh", "r") as file:
                data += file.read()
    with open("./dict/end_part", "r") as file:
        data += file.read()
    data = data.replace(search_text, addon_name)
    with open(addon_path + addon_name + "/lua/autorun/" + addon_name + "_autorun.lua", 'w+') as file:
        file.write(data) 


def build_folder():
    addon_name = addon_name_var.get()  # Récupérer l'addon_name depuis le StringVar
    main_folder = Path(addon_path + addon_name + "/lua/autorun")
    addons_body = Path(addon_path + addon_name + "/lua/" + addon_name)
    try:
        main_folder.mkdir(parents=True, exist_ok=True)
        addons_body.mkdir(parents=True, exist_ok=True)
        if server.get():
            server_path = Path(addon_path + addon_name + "/lua/" + addon_name + "/server")
            server_path.mkdir(parents=True, exist_ok=True)
        else:
            print("not server")
        if client.get():
            client_path = Path(addon_path + addon_name + "/lua/" + addon_name + "/client")
            client_path.mkdir(parents=True, exist_ok=True)
        if shared.get():
            shared_path = Path(addon_path + addon_name + "/lua/" + addon_name + "/config")
            shared_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory created successfully.")
        print(addon_path + addon_name)
    except FileExistsError:
        print(f"Directory already exists.")
        exit(1)
    except PermissionError:
        print(f"Permission denied: Unable to create.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
    build_files()
    top.destroy()


def selectaddonfolder():
    global addon_path
    addon_path =  askdirectory(title="Choisissez un dossier") + "/"
    path_label.config(text=addon_path)

def draw_window():
    global addon_name_var  # Utiliser addon_name_var
    top.geometry("500x300")
    top.title("Créateur d'addon GMod")

    global path_label
    path_label = Label(top, text="Selectionnez le dossier de création de l'addon")
    path_label.pack(pady=10)

    select_button = Button(top, text="Choisir dossier", command=selectaddonfolder)
    select_button.pack(pady=10)

    Checkbutton(top, text='Inclure serveur', variable=server).place(x=200, y=90)
    Checkbutton(top, text='Inclure client', variable=client).place(x=200, y=120)
    Checkbutton(top, text='Inclure config', variable=shared).place(x=200, y=150)

    name_label = Label(top, text="Entrez le nom de l'addon :")
    name_label.place(x=100, y=200)
    name_entry = Entry(top, textvariable = addon_name_var, font=('calibre',10,'normal')).place(x=250, y=200)

    sub_btn= Button(top, text = "Créer l'addon", command = build_folder)
    sub_btn.place(x=210, y=250)

    top.mainloop()

draw_window()
