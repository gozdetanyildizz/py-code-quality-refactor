import subprocess
from typing import Tuple

def run_cmd(cmd: list[str]) -> Tuple[int, str, str]:
    """
    Dış komutu çalıştırır; (returncode, stdout, stderr) döner.
    """
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr
