import argparse
import sys
import os
from PyQt5 import QtWidgets, QtGui
from win import Ui_MainWindow
import mxlrc

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
        artist = self.Artist_in.text()
        title = self.Title_in.text()
        output_dir = self.Output_in.text()
        sleep_time = int(self.Sleep_in.text()) if self.Sleep_in.text() else 30
        max_depth = int(self.Depth_in.text()) if self.Depth_in.text() else 100
        update_mode = self.Update_chk.isChecked()
        bfs_mode = self.bfs_chk.isChecked()
        token_input = self.Token_in.text()

        # 如果 token_input 為空，則使用從 token.txt 中讀取的 token
        token = token_input if token_input else self.token

        if not token:
            self.info.setText("Token is empty. No action performed.")
            return

        args = argparse.Namespace(
            song=[f"{artist},{title}"],
            outdir=output_dir,
            sleep=sleep_time,
            depth=max_depth,
            update=update_mode,
            bfs=bfs_mode,
            token=token,
            quiet=False,
            debug=False
        )

        args = mxlrc.init_args(args)

        song = mxlrc.Song(artist, title)
        musixmatch = mxlrc.Musixmatch(token=token)

        body = musixmatch.find_lyrics(song)
        if not body:
            self.info.setText("Lyrics not found or an error occurred.")
            return

        song.update_info(body)

        if not mxlrc.Musixmatch.get_synced(song, body):
            mxlrc.Musixmatch.get_unsynced(song, body)

        success = mxlrc.Musixmatch.gen_lrc(song, outdir=args.outdir)
        if success:
            self.info.setText(f"LRC file generated successfully in {args.outdir}\nDone")
        else:
            self.info.setText("Failed to generate LRC file.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
