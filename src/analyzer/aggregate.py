from .models import AnalysisResult, Issue
from .pylint_runner import run_pylint
from .flake8_runner import run_flake8
from .radon_runner import run_radon_cc

def analyze_file(path: str) -> AnalysisResult:
    issues: list[Issue] = []
    # Her bir aracı çalıştır
    try:
        issues.extend(run_pylint(path))
    except Exception as e:
        issues.append(Issue("pylint", path, 1, 0, "PYLINT-ERROR", f"Pylint çalışırken hata: {e}", "error"))
    try:
        issues.extend(run_flake8(path))
    except Exception as e:
        issues.append(Issue("flake8", path, 1, 0, "FLAKE8-ERROR", f"Flake8 çalışırken hata: {e}", "error"))
    try:
        issues.extend(run_radon_cc(path))
    except Exception as e:
        issues.append(Issue("radon", path, 1, 0, "RADON-ERROR", f"Radon çalışırken hata: {e}", "error"))
    return AnalysisResult(issues=issues)
