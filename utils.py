import os
import webbrowser
import sys
import json
from PyQt5 import QtWidgets, QtCore

configfile_resource = QtCore.QFile(":/rsc/config.json")
configfile_local = "config.json"

def toggle_dark_mode(app, main_window, is_dark_mode):
    try:
        if is_dark_mode:
            app.setStyleSheet("")
            main_window.log_info("Theme switched to light mode.")
        else:
            qss_file = QtCore.QFile(":/rsc/stylesheet.qss")
            if qss_file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
                stream = QtCore.QTextStream(qss_file)
                qss = stream.readAll()
                app.setStyleSheet(qss)
                main_window.log_info("Theme switched to dark mode.")
            else:
                main_window.log_error("Failed to load stylesheet.qss")
                return is_dark_mode
    except Exception as e:
        main_window.log_error(f"Error while toggling theme: {e}")

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
        extract_resource_config(configfile_local)

    with open(configfile_local, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_resource_config(destination):
    config_resource = QtCore.QFile(":/rsc/config.json")
    if config_resource.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
        config_data = config_resource.readAll().data().decode('utf-8')
        config_resource.close()

        with open(destination, "w", encoding="utf-8") as file:
            file.write(config_data)
    else:
        raise Exception("Unable to open config.json from resources.")

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
