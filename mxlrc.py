import subprocess
from utils import build_args_list

def run_subprocess(command, log_info, log_error):
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace'
        )
        stdout, stderr = process.communicate()

        if stdout:
            log_info(stdout.strip())
        if stderr:
            log_error(stderr.strip())

        if process.returncode != 0:
            log_error(f"Failed to process with exit code {process.returncode}.")
        else:
            log_info("Process completed successfully.")
    except Exception as e:
        log_error(f"Failed to start process: {e}")

def download_lrc(self, search_string, output_dir, sleep_time, max_depth, token, directory_mode=False):
    args_list = build_args_list(search_string, output_dir, sleep_time, max_depth, token,
                                self.Quiet_chk.isChecked(), self.Update_chk.isChecked(), self.bfs_chk.isChecked(), directory_mode)
    self.info.append(f"[D] Arguments: {args_list}")
    run_subprocess(['mxlrc.exe'] + args_list, self.log_info, self.log_error)
