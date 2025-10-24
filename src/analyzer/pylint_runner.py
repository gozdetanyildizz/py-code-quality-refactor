import json
from typing import List
from .models import Issue
from .utils import run_cmd

def run_pylint(path: str) -> List[Issue]:
    """
    Pylint'i alt süreçte JSON formatında çalıştırır ve Issue listesi döndürür.
    Bu yöntem Pylint'in konsola yazmasını engeller (çıktıyı biz yakalıyoruz).
    """
    # --score=n: skor satırını kapatır; -f json: JSON çıktı
    rc, out, err = run_cmd(["python", "-m", "pylint", path, "-f", "json", "--score=n"])

    # Pylint bazı durumlarda boş string döndürebilir
    if not out.strip():
        return []

    issues: List[Issue] = []
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        # Beklenmeyen durumlarda stderr'i bir Issue olarak ekleyelim
        return [Issue("pylint", path, 1, 0, "PYLINT-JSON-ERROR", f"JSON parse hatası: {err or out}", "error")]

    # Çıktı ya liste (çoklu ihlal) ya da tek obje olabiliyor
    if isinstance(data, dict):
        data = [data]

    for item in data:
        issues.append(
            Issue(
                tool="pylint",
                path=item.get("path", path),
                line=int(item.get("line", 1) or 1),
                col=int(item.get("column", 0) or 0),
                code=item.get("message-id", item.get("symbol", "PYLINT")),
                message=item.get("message", ""),
                severity=item.get("type", None),  # convention/warning/error/refactor vb.
            )
        )
    return issues
