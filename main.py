import subprocess
import webbrowser
import sys
import os
from PyQt5 import QtWidgets, QtGui
from mutagen import File
from win import Ui_MainWindow

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        version = 'std'
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/ico/icon.png'))
        self.pushButton.clicked.connect(self.start_process)

        self.actionExit.triggered.connect(self.close)
        self.actionOpen_Folder_2.triggered.connect(self.open_folder)
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionAbout.triggered.connect(self.show_about)
        self.actionUpdate.triggered.connect(self.check_for_update)

        if version == 'gui':
            self.check_mxlrc_existence()

        self.token = ""
        token_file_path = "token.txt"

        if os.path.exists(token_file_path):
            try:
                with open(token_file_path, "r") as token_file:
                    self.token = token_file.read().strip()
            except Exception as e:
                print(f"Error reading token file: {e}")

        self.Token_in.setText(self.token)

    def check_mxlrc_existence(self):
        if not os.path.exists('./mxlrc.exe'):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Missing File")
            msg.setText("The required file 'mxlrc.exe' is not found in the current directory.")
            msg.setInformativeText("Please download 'mxlrc.exe' and place it in the same directory as this application.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            sys.exit()

    def start_process(self):
        self.info.setText("")
        artist = self.Artist_in.text()
        title = self.Title_in.text()
        output_dir = self.Output_in.text()
        sleep_time = int(self.Sleep_in.text()) if self.Sleep_in.text() else 30
        max_depth = int(self.Depth_in.text()) if self.Depth_in.text() else 100
        token_input = self.Token_in.text()

        token = token_input if token_input else self.token

        if not token:
            self.info.append("Token is empty. No action performed.")
            return

        args_list = [
            'mxlrc.exe',
            '-s', f"{artist},{title}",
            '-o', output_dir,
            '-t', str(sleep_time),
            '-d', str(max_depth),
            '--token', token
        ]

        if self.Quiet_chk.isChecked():
            args_list.append('-q')
        if self.Update_chk.isChecked():
            args_list.append('-u')
        if self.bfs_chk.isChecked():
            args_list.append('--bfs')

        try:
            process = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            self.info.append(f"[DEBUG] Args: {args_list}")
            if stdout:
                self.info.append(stdout)
            if stderr:
                self.info.append(stderr)

            if process.returncode == 0:
                self.info.append("Process completed successfully.")
            else:
                self.info.append(f"Process failed with exit code {process.returncode}.")
        except Exception as e:
            self.info.append(f"[DEBUG] Args: {args_list}")
            self.info.append(f"Error occurred: {e}")

    def open_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            self.info.append(f"Selected Folder: {folder_path}")

    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Audio Files (*.mp3 *.flac *.wav *.ogg *.m4a)")
        if file_path:
            self.info.append(f"Selected File: {file_path}")
            self.load_metadata(file_path)

    def load_metadata(self, file_path):
        self.info.setText("")
        try:
            audio_file = File(file_path)
            if audio_file:
                artist = audio_file.get('ARTIST', [''])[0]
                title = audio_file.get('TITLE', [''])[0]
                self.Artist_in.setText(artist)
                self.Title_in.setText(title)
                self.info.append(f"Loaded metadata - Artist: {artist}, Title: {title}")
            else:
                self.info.append("No metadata found in the file.")
        except Exception as e:
            self.info.append(f"Failed to load metadata: {e}")

    def show_about(self):
        QtWidgets.QMessageBox.about(self, "About", "GMxLRC v1.2 by ElliotCHEN37\nMxLRC v1.2.2 by fashni\n"
                                                   "Licensed under MIT License")

    def check_for_update(self):
        webbrowser.open('https://github.com/ElliotCHEN37/GMxLRC/releases/latest')

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
