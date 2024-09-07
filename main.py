import warnings
import webbrowser
import sys
import os
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
from tinytag import TinyTag
from win import Ui_MainWindow

warnings.filterwarnings("ignore", category=DeprecationWarning)

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/ico/icon.png'))

        self.fontDB = QtGui.QFontDatabase()
        self.fontDB.addApplicationFont(":/fnt/JetBrainsMono-Light.ttf")
        self.info.setFont(QtGui.QFont("JetBrains Mono Light", 7))

        self.setup_connections()
        self.check_executable()

        self.token = self.load_token()
        self.Token_in.setText(self.token)

    def setup_connections(self):
        self.pushButton.clicked.connect(self.start_process)
        self.actionExit.triggered.connect(self.close)
        self.actionOpen_Folder.triggered.connect(self.open_folder)
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionAbout.triggered.connect(self.show_about)
        self.actionUpdate.triggered.connect(self.cfu)
        self.actionBd.triggered.connect(self.open_batch_file)
        self.actionLicense.triggered.connect(self.license_popup)

    def check_executable(self):
        if not os.path.exists('mxlrc.exe'):
            QtWidgets.QMessageBox.warning(
                self, "Missing File",
                "The required file 'mxlrc.exe' is not found in the current directory.\n"
                "Please download 'mxlrc.exe' and place it in the same directory as this application."
            )
            webbrowser.open('https://github.com/fashni/MxLRC/releases/latest')
            sys.exit()

    def load_token(self):
        try:
            with open("token.txt", "r", encoding="utf-8") as token_file:
                return token_file.read().strip()
        except Exception as e:
            self.log_error(f"Error reading token file: {e}")
            return ""

    def start_process(self):
        artist, title, output_dir = self.get_inputs()
        sleep_time, max_depth, token = self.get_processing_params()

        if not token:
            self.log_info("Token is empty. No action performed.")
            return

        search_string = f'"{artist},{title}"'
        self.download_lrc(search_string, output_dir, sleep_time, max_depth, token)

    def get_inputs(self):
        return (self.Artist_in.text().strip(),
                self.Title_in.text().strip(),
                self.Output_in.text().strip())

    def get_processing_params(self):
        return (int(self.Sleep_in.text()),
                int(self.Depth_in.text()),
                self.Token_in.text().strip() or self.token)

    def build_args_list(self, search_string, output_dir, sleep_time, max_depth, token, directory_mode=False):
        args_list = ['-s', search_string, '--token', token]
        args_list += ['-t', str(sleep_time), '-d', str(max_depth)] if directory_mode else ['-o', output_dir]

        if self.Quiet_chk.isChecked(): args_list.append('-q')
        if self.Update_chk.isChecked(): args_list.append('-u')
        if self.bfs_chk.isChecked(): args_list.append('--bfs')

        return args_list

    def download_lrc(self, search_string, output_dir, sleep_time, max_depth, token, directory_mode=False):
        args_list = self.build_args_list(search_string, output_dir, sleep_time, max_depth, token, directory_mode)
        self.info.append(f"[D] Arguments: {args_list}")
        self.run_subprocess(['mxlrc.exe'] + args_list)

    def run_subprocess(self, command):
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace'
            )
            stdout, stderr = process.communicate()

            if stdout: self.log_info(stdout.strip())
            if stderr: self.log_error(stderr.strip())

            if process.returncode != 0:
                self.log_error(f"Failed to process with exit code {process.returncode}.")
            else:
                self.log_info("Process completed successfully.")
        except Exception as e:
            self.log_error(f"Failed to start process: {e}")

    def open_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            self.log_info(f"Selected Folder: {folder_path}")
            _, _, token = self.get_processing_params()
            if not token:
                self.log_info("Token is empty. No action performed.")
                return
            self.download_lrc(folder_path, "", *self.get_processing_params(), directory_mode=True)

    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Audio Files (*.mp3 *.flac *.wav *.ogg *.m4a)")
        if file_path:
            self.log_info(f"Selected File: {file_path}")
            try:
                audio_file = TinyTag.get(file_path)
                artist, title = audio_file.artist or '', audio_file.title or ''
                self.Artist_in.setText(artist)
                self.Title_in.setText(title)
                self.log_info(f"Loaded metadata - Artist: {artist}, Title: {title}")
            except Exception as e:
                self.log_error(f"Failed to load metadata: {e}")

    def open_batch_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Song List", "", "Text Files (*.txt)")
        if file_path:
            self.log_info(f"Selected Song List: {file_path}")
            self.process_batch_file(file_path)

    def process_batch_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as batch_file:
                lines = batch_file.readlines()
                output_dir, sleep_time, max_depth, token = self.Output_in.text().strip(), *self.get_processing_params()

                if not token:
                    self.log_info("Token is empty. No action performed.")
                    return

                for line in lines:
                    artist, title = [s.strip() for s in line.split(',')]
                    self.download_lrc(f'"{artist},{title}"', output_dir, sleep_time, max_depth, token)
                    self.log_info(f"Processing: {artist} - {title}")
        except Exception as e:
            self.log_error(f"Failed to process: {e}")

    def show_about(self):
        QtWidgets.QMessageBox.about(self, "About", "GMxLRC v1.4.1 by ElliotCHEN37\nLicensed under MIT License")

    @staticmethod
    def cfu():
        webbrowser.open('https://github.com/ElliotCHEN37/GMxLRC/releases/latest')

    def license_popup(self):
        try:
            license_file = QtCore.QFile(":/lnc/LICENSE")
            if license_file.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
                license_text = QtCore.QTextStream(license_file).readAll()
                license_file.close()
                QtWidgets.QMessageBox.information(self, "License", license_text)
            else:
                raise Exception("Unable to open resource file.")
        except Exception as e:
            self.log_error(f"Failed to load license file: {e}")

    def log_info(self, message):
        self.info.append(f"[I] {message}")

    def log_error(self, message):
        self.info.append(f"[E] {message}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
