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
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/ico/icon.png'))
        self.pushButton.clicked.connect(self.start_process)

        self.actionExit.triggered.connect(self.close)
        self.actionOpen_Folder_2.triggered.connect(self.open_folder)
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionAbout.triggered.connect(self.show_about)
        self.actionUpdate.triggered.connect(self.check_for_update)

        if not os.path.exists('./mxlrc.exe'):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Missing File")
            msg.setText("The required file 'mxlrc.exe' is not found in the current directory.")
            msg.setInformativeText(
                "Please download 'mxlrc.exe' and place it in the same directory as this application.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            sys.exit()

        self.token = ""

        if os.path.exists("token.txt"):
            try:
                with open("token.txt", "r") as token_file:
                    self.token = token_file.read().strip()
            except Exception as e:
                print(f"Error reading token file: {e}")

        self.Token_in.setText(self.token)


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

        self.download_lrc(artist, title, output_dir, sleep_time, max_depth, token)

    def download_lrc(self, artist, title, output_dir, sleep_time, max_depth, token):
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
                self.info.append(f"Downloaded LRC for {artist} - {title}")
            else:
                self.info.append(f"Failed to download LRC for {artist} - {title} with exit code {process.returncode}.")
        except Exception as e:
            self.info.append(f"[DEBUG] Args: {args_list}")
            self.info.append(f"Error occurred: {e}")

    def open_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            self.info.append(f"Selected Folder: {folder_path}")
            self.batch_process_folder(folder_path)

    def batch_process_folder(self, folder_path):
        supported_formats = ('.mp3', '.flac', '.wav', '.ogg', '.m4a')
        audio_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_formats)]

        if not audio_files:
            self.info.append("No audio files found in the selected folder.")
            return

        output_dir = self.Output_in.text()
        sleep_time = int(self.Sleep_in.text()) if self.Sleep_in.text() else 30
        max_depth = int(self.Depth_in.text()) if self.Depth_in.text() else 100
        token = self.Token_in.text() or self.token

        if not token:
            self.info.append("Token is empty. No action performed.")
            return

        for audio_file in audio_files:
            file_path = os.path.join(folder_path, audio_file)
            try:
                audio = File(file_path)
                artist = audio.get('ARTIST', ['Unknown Artist'])[0]
                title = audio.get('TITLE', [os.path.splitext(audio_file)[0]])[0]
                self.info.append(f"Processing file: {audio_file} (Artist: {artist}, Title: {title})")
                self.download_lrc(artist, title, output_dir, sleep_time, max_depth, token)
            except Exception as e:
                self.info.append(f"Failed to process file {audio_file}: {e}")

    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",
                                                             "Audio Files (*.mp3 *.flac *.wav *.ogg *.m4a)")
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
