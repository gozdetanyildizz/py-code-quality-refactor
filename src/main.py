from src.analyzer.aggregate import analyze_file
from src.refactor_suggestions.rules import generate_suggestions
import sys
from pathlib import Path

def _print_report(path: str):
    result = analyze_file(path)
    print(f"\nAnaliz: {path}")
    print("-" * 60)
    if not result.issues:
        print("Sorun bulunamadı 🎉")
        return
    for it in result.issues:
        print(f"[{it.tool}] {it.path}:{it.line}:{it.col} {it.code} -> {it.message}")
    print("\nÖneriler:")
    for s in generate_suggestions(result.issues):
        print(f" - {s}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python -m src.main <dosya_yolu>")
        sys.exit(1)
    target = sys.argv[1]
    if not Path(target).exists():
        print(f"Dosya bulunamadı: {target}")
        sys.exit(1)
    _print_report(target)
