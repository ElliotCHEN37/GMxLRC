from tinytag import TinyTag
from PyQt5 import QtWidgets

def load_metadata(file_path):
    try:
        audio_file = TinyTag.get(file_path)
        artist, title = audio_file.artist or '', audio_file.title or ''
        return artist, title
    except Exception as e:
        raise Exception(f"Failed to load metadata: {e}")

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
            artist, title = load_metadata(file_path)
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
