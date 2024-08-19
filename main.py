import subprocess
import sys
import os
from PyQt5 import QtWidgets, QtGui
from win import Ui_MainWindow

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/ico/icon.png'))
        self.pushButton.clicked.connect(self.start_process)

        self.token = ""
        token_file_path = "token.txt"

        if os.path.exists(token_file_path):
            try:
                with open(token_file_path, "r") as token_file:
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

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
