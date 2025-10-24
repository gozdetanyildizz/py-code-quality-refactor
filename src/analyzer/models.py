from dataclasses import dataclass
from typing import Optional

@dataclass
class Issue:
    tool: str                 # 'pylint' | 'flake8' | 'radon'
    path: str
    line: int
    col: int
    code: str                 # örn. 'C0103' (pylint), 'E302' (flake8), 'CC' (radon)
    message: str
    severity: Optional[str] = None  # 'info' | 'warning' | 'error' | 'refactor' | 'convention'

@dataclass
class AnalysisResult:
    issues: list[Issue]