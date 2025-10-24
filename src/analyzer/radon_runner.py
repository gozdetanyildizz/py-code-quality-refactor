from typing import List
from radon.complexity import cc_visit  # pip ile kurulu (radon)
from .models import Issue

_BAD_RANKS = {"C", "D", "E", "F"}  # Uyarı üretilecek dereceler

def run_radon_cc(path: str) -> List[Issue]:
    """
    Radon ile cyclomatic complexity ölçer.
    C ve daha kötü dereceleri Issue olarak döndürür.
    """
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    blocks = cc_visit(code)
    issues: List[Issue] = []
    for b in blocks:
        rank = getattr(b, "rank", None)
        if rank in _BAD_RANKS:
            issues.append(
                Issue(
                    tool="radon",
                    path=path,
                    line=getattr(b, "lineno", 1) or 1,
                    col=0,
                    code=f"CC-{rank}",
                    message=f"{b.name} fonksiyonunun karmaşıklığı {b.complexity} (rank {rank}).",
                    severity="warning" if rank in {"C", "D"} else "error",
                )
            )
    return issues
