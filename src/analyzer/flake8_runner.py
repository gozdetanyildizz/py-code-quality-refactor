import re
from typing import List
from .models import Issue
from .utils import run_cmd

_LINE_RE = re.compile(r"^(.*?):(\d+):(\d+):\s*([A-Z]\d{3})\s*(.*)$")

def run_flake8(path: str) -> List[Issue]:
    """
    Flake8'i alt süreç olarak çağırır ve standart metin çıktısını ayrıştırır.
    Format beklenen: file:line:col: CODE message
    """
    # --extend-ignore veya config dosyası sonradan eklenebilir
    rc, out, _ = run_cmd(["python", "-m", "flake8", path])
    issues: List[Issue] = []
    for line in out.splitlines():
        m = _LINE_RE.match(line.strip())
        if not m:
            continue
        fpath, ln, col, code, msg = m.groups()
        issues.append(
            Issue(
                tool="flake8",
                path=fpath,
                line=int(ln),
                col=int(col),
                code=code,
                message=msg,
                severity="warning" if code.startswith(("W", "C", "E")) else "info",
            )
        )
    return issues
