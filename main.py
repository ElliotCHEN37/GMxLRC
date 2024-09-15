import warnings
from win import *
from aud import *
from mxlrc import *
from utils import *

warnings.filterwarnings("ignore", category=DeprecationWarning)

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.is_dark_mode = self.config.get("darkmode", "0") == "1"  # Read dark mode setting

        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/ico/icon.png'))

        self.fontDB = QtGui.QFontDatabase()
        self.fontDB.addApplicationFont(":/fnt/JetBrainsMono-Light.ttf")
        self.info.setFont(QtGui.QFont("JetBrains Mono Light", 7))

        apply_config(self.config, self)
        self.apply_stylesheet()  # Apply the stylesheet based on the current mode

        self.setup_connections()
        check_executable('mxlrc.exe')

    def apply_stylesheet(self):
        if self.is_dark_mode:
            self.setStyleSheet(dark_mode_stylesheet)
        else:
            self.setStyleSheet("")  # Reset to default stylesheet

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
        self.actionDarkT.triggered.connect(self.toggle_dark_mode)

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
                self.Token_in.text().strip() or self.config.get('token', ''))

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

    def toggle_dark_mode(self):
        self.is_dark_mode = toggle_dark_mode(self, self, self.is_dark_mode)
        self.apply_stylesheet()  # Apply the stylesheet based on the new mode
        self.restart_app()  # Restart the app to apply platform changes

    def restart_app(self):
        # Save the current state to a config file or environment variable
        self.config["darkmode"] = "1" if self.is_dark_mode else "0"
        with open("config.json", "w", encoding="utf-8") as file:
            json.dump(self.config, file, indent=4, ensure_ascii=False)

        # Close the current application
        QtWidgets.QApplication.quit()

        # Relaunch the application
        new_args = sys.argv + [f'-platform', f'windows:darkmode={int(self.is_dark_mode)}']
        QtCore.QProcess.startDetached(sys.executable, new_args)

    def log_info(self, message):
        self.info.append(f"[I] {message}")

    def log_error(self, message):
        self.info.append(f"[E] {message}")

if __name__ == "__main__":
    darknum = int(load_config().get("darkmode", "0"))  # Read dark mode config
    app = QtWidgets.QApplication(sys.argv + [f'-platform', f'windows:darkmode={darknum}'])
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
