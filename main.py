import warnings
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import webbrowser
from win import Ui_MainWindow
from aud import open_folder, open_file, open_batch_file, process_batch_file
from mxlrc import download_lrc
from utils import check_executable, load_token

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
        check_executable('mxlrc.exe')

        self.token = load_token("token.txt")
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
        self.actionChangelog.triggered.connect(self.show_changelog)

    def start_process(self):
        artist, title, output_dir = self.get_inputs()
        sleep_time, max_depth, token = self.get_processing_params()

        if not token:
            self.log_info("Token is empty. No action performed.")
            return

        search_string = f'"{artist},{title}"'
        download_lrc(self, search_string, output_dir, sleep_time, max_depth, token)

    def get_inputs(self):
        return (self.Artist_in.text().strip(),
                self.Title_in.text().strip(),
                self.Output_in.text().strip())

    def get_processing_params(self):
        return (int(self.Sleep_in.text()),
                int(self.Depth_in.text()),
                self.Token_in.text().strip() or self.token)

    def open_folder(self):
        open_folder(self)

    def open_file(self):
        open_file(self)

    def open_batch_file(self):
        open_batch_file(self)

    def process_batch_file(self, file_path):
        process_batch_file(self, file_path)

    def show_about(self):
        QtWidgets.QMessageBox.about(self, "About", "GMxLRC v1.5 by ElliotCHEN37\nLicensed under MIT License")

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

    def show_changelog(self):
        QtWidgets.QMessageBox.information(self, "Changelog", "v1.5\n-Separate different parts from main.py")

    def log_info(self, message):
        self.info.append(f"[I] {message}")

    def log_error(self, message):
        self.info.append(f"[E] {message}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
