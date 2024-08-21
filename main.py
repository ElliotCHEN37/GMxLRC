import webbrowser
import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from mutagen import File
from win import Ui_MainWindow


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/ico/icon.png'))

        self.fontDB = QtGui.QFontDatabase()
        self.fontDB.addApplicationFont(":/fnt/JetBrainsMono-Light.ttf")
        self.info.setFont(QtGui.QFont("JetBrains Mono Light", 7))

        self.pushButton.clicked.connect(self.start_process)
        self.actionExit.triggered.connect(self.close)
        self.actionOpen_Folder.triggered.connect(self.open_folder)
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionAbout.triggered.connect(self.show_about)
        self.actionUpdate.triggered.connect(self.check_for_update)
        self.actionBd.triggered.connect(self.open_batch_file)
        self.actionLicense.triggered.connect(self.license_popup)

        self.check_executable()

        self.token = self.load_token()
        self.Token_in.setText(self.token)

        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def check_executable(self):
        if not os.path.exists('mxlrc.exe'):
            QtWidgets.QMessageBox.warning(
                self,
                "Missing File",
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
            print(f"Error reading token file: {e}")
            return ""

    def start_process(self):
        artist_input = self.Artist_in.text().strip()
        title_input = self.Title_in.text().strip()
        output_dir = self.Output_in.text().strip()
        sleep_time = int(self.Sleep_in.text())
        max_depth = int(self.Depth_in.text())
        token = self.Token_in.text().strip() or self.token

        if not token:
            if not self.Quiet_chk.isChecked():
                self.info.append("Token is empty. No action performed.")
            return

        search_string = f'"{artist_input},{title_input}"'
        self.download_lrc(search_string, output_dir, sleep_time, max_depth, token)

    def download_lrc(self, search_string, output_dir, sleep_time, max_depth, token, directory_mode=False):
        args_list = [
            '-s', search_string, '--token', token
        ]

        if directory_mode:
            args_list = ['-s', search_string, '-t', str(sleep_time), '-d', str(max_depth), '--token', token]
        else:
            args_list.append('-o')
            args_list.append(output_dir)

        if self.Quiet_chk.isChecked():
            args_list.append('-q')
        if self.Update_chk.isChecked():
            args_list.append('-u')
        if self.bfs_chk.isChecked():
            args_list.append('--bfs')

        self.info.append(f"[D] Arguments: {str(args_list)}")

        self.process.start('mxlrc.exe', args_list)

    def handle_stdout(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.info.append(f"[I] {output.strip()}")

    def handle_stderr(self):
        error = self.process.readAllStandardError().data().decode()
        self.info.append(f"[E] {error.strip()}")

    def process_finished(self):
        if self.process.exitCode() != 0 and not self.Quiet_chk.isChecked():
            self.info.append(f"[X] Failed to process with exit code {self.process.exitCode()}.")

    def handle_process_output(self, process):
        for stdout_line in iter(process.stdout.readline, ''):
            if stdout_line:
                self.info.append(f"[I] {stdout_line.strip()}")
        for stderr_line in iter(process.stderr.readline, ''):
            if stderr_line:
                self.info.append(f"{stderr_line.strip()}")
        process.stdout.close()
        process.stderr.close()
        process.wait()

        if process.returncode != 0 and not self.Quiet_chk.isChecked():
            self.info.append(f"[X] Failed to process with exit code {process.returncode}.")

    def open_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            self.info.append(f"Selected Folder: {folder_path}")

            sleep_time = int(self.Sleep_in.text())
            max_depth = int(self.Depth_in.text())
            token = self.Token_in.text().strip() or self.token

            if not token:
                self.info.append("Token is empty. No action performed.")
                return

            search_string = folder_path

            self.download_lrc(search_string, "", sleep_time, max_depth, token, directory_mode=True)

    def process_audio_file(self, file_path, output_dir, sleep_time, max_depth, token):
        try:
            audio = File(file_path)
            artist = audio.get('ARTIST', ['Unknown Artist'])[0]
            title = audio.get('TITLE', [os.path.splitext(os.path.basename(file_path))[0]])[0]
            self.info.append(f"Processing file: {file_path} (Artist: {artist}, Title: {title})")
            self.download_lrc(f'"{artist},{title}"', output_dir, sleep_time, max_depth, token)
        except Exception as e:
            self.info.append(f"Failed to process file {file_path}: {e}")

    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",
                                                             "Audio Files (*.mp3 *.flac *.wav *.ogg *.m4a)")
        if file_path:
            self.info.append(f"Selected File: {file_path}")
            try:
                audio_file = File(file_path)
                artist = audio_file.get('ARTIST', [''])[0]
                title = audio_file.get('TITLE', [''])[0]
                self.Artist_in.setText(artist)
                self.Title_in.setText(title)
                self.info.append(f"Loaded metadata - Artist: {artist}, Title: {title}")
            except Exception as e:
                self.info.append(f"Failed to load metadata: {e}")

    def open_batch_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Song List", "", "Text Files (*.txt)")
        if file_path:
            self.info.append(f"Selected Song List: {file_path}")
            try:
                with open(file_path, "r", encoding="utf-8") as batch_file:
                    lines = batch_file.readlines()
                    output_dir = self.Output_in.text().strip()
                    sleep_time = int(self.Sleep_in.text() or 30)
                    max_depth = int(self.Depth_in.text() or 100)
                    token = self.Token_in.text().strip() or self.token

                    if not token:
                        self.info.append("Token is empty. No action performed.")
                        return

                    for line in lines:
                        artist, title = [s.strip() for s in line.split(',')]
                        self.download_lrc(f'"{artist},{title}"', output_dir, sleep_time, max_depth, token)
                        self.info.append(f"Processing: {artist} - {title}")
            except Exception as e:
                self.info.append(f"Failed to process: {e}")

    def show_about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    "GMxLRC v1.4 by ElliotCHEN37\nLicensed under MIT License")

    def check_for_update(self):
        webbrowser.open('https://github.com/ElliotCHEN37/GMxLRC/releases/latest')

    def license_popup(self):
        QtWidgets.QMessageBox.information(self, "License", "This program (GMxLRC) was licensed under MIT License\n\n"
                                                           "MIT License\n"
                                                           "Copyright (c) 2024 Elliot\n\n"
                                                           "Permission is hereby granted, free of charge, to any person obtaining a copy "
                                                           'of this software and associated documentation files (the "Software"), to deal '
                                                           "in the Software without restriction, including without limitation the rights "
                                                           "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
                                                           "copies of the Software, and to permit persons to whom the Software is "
                                                           "furnished to do so, subject to the following conditions:\n\n"
                                                           "1. The original author and the authors of any other software used with this "
                                                           "software must be credited\n\n"
                                                           "The above copyright notice and this permission notice shall be included in all "
                                                           "copies or substantial portions of the Software.\n\n"
                                                           'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR '
                                                           "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
                                                           "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
                                                           "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
                                                           "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
                                                           "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
                                                           "SOFTWARE.\n\n"
                                                           "JetBrains Mono Light font was licensed under SIL Open Font License 1.1\n\n"
                                                           "PyQt5 was licensed under GPL v3 License\n\n"
                                                           "mutagen was licensed under GPL v2 or later")


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
