import os
import webbrowser
import sys
import json
from PyQt5 import QtWidgets, QtCore

configfile_resource = ":/rsc/config.json"
configfile_local = "config.json"

def toggle_dark_mode(app, main_window, is_dark_mode):
    if is_dark_mode:
        app.setStyleSheet("")
        main_window.log_info("Theme switched.")
    else:
        app.setStyleSheet(configfile_resource)
        main_window.log_info("Theme switched.")
    return not is_dark_mode

def check_executable(file_name):
    if not os.path.exists(file_name):
        QtWidgets.QMessageBox.warning(
            None, "Missing File",
            f"The required file '{file_name}' is not found in the current directory.\n"
            "Please download the file and place it in the same directory as this application."
        )
        webbrowser.open('https://github.com/fashni/MxLRC/releases/latest')
        sys.exit()

def build_args_list(search_string, output_dir, sleep_time, max_depth, token, quiet, update, bfs, directory_mode=False):
    args_list = ['-s', search_string, '--token', token]
    if directory_mode:
        args_list += ['-t', str(sleep_time), '-d', str(max_depth)]
    else:
        args_list += ['-o', output_dir]

    if quiet:
        args_list.append('-q')
    if update:
        args_list.append('-u')
    if bfs:
        args_list.append('--bfs')

    return args_list

def load_config():
    if not os.path.exists(configfile_local):
        create_default_config()

    with open(configfile_local, "r", encoding="utf-8") as file:
        config = json.load(file)

    return config

def create_default_config():
    with open(configfile_resource, "w", encoding="utf-8") as file:
        json.dump(configfile_resource, file, indent=4, ensure_ascii=False)

def apply_config(config, main_window):
    main_window.Token_in.setText(config.get("token", ""))
    dark_mode = config.get("darkmode", "0") == "1"
    quiet = config.get("quiet", "0") == "1"
    update = config.get("update", "0") == "1"
    bfs = config.get("bfs", "0") == "1"
    sleep_time = int(config.get("sleep", "30"))
    max_depth = int(config.get("depth", "100"))
    output_dir = config.get("output", "lyrics")

    main_window.Quiet_chk.setChecked(quiet)
    main_window.Update_chk.setChecked(update)
    main_window.bfs_chk.setChecked(bfs)
    main_window.Sleep_in.setText(str(sleep_time))
    main_window.Depth_in.setText(str(max_depth))
    main_window.Output_in.setText(output_dir)

    if dark_mode:
        toggle_dark_mode(main_window, main_window, dark_mode)
        main_window.is_dark_mode = True
