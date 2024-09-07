import os
import webbrowser
import sys
from PyQt5 import QtWidgets

def check_executable(file_name):
    if not os.path.exists(file_name):
        QtWidgets.QMessageBox.warning(
            None, "Missing File",
            f"The required file '{file_name}' is not found in the current directory.\n"
            "Please download the file and place it in the same directory as this application."
        )
        webbrowser.open('https://github.com/fashni/MxLRC/releases/latest')
        sys.exit()

def load_token(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as token_file:
            return token_file.read().strip()
    except Exception as e:
        raise Exception(f"Error reading token file: {e}")

def build_args_list(search_string, output_dir, sleep_time, max_depth, token, quiet, update, bfs, directory_mode=False):
    args_list = ['-s', search_string, '--token', token]
    args_list += ['-t', str(sleep_time), '-d', str(max_depth)] if directory_mode else ['-o', output_dir]

    if quiet: args_list.append('-q')
    if update: args_list.append('-u')
    if bfs: args_list.append('--bfs')

    return args_list
