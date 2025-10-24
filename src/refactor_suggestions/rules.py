from typing import Iterable, List
from src.analyzer.models import Issue

def generate_suggestions(issues: Iterable[Issue]) -> List[str]:
    """
    Çok basit kural tabanlı öneriler.
    İleride AST tabanlı ve pattern-mining ile zenginleştirilebilir.
    """
    suggestions: list[str] = []
    for it in issues:
        # Radon karmaşıklık
        if it.tool == "radon" and it.code.startswith("CC-"):
            suggestions.append(
                f"{it.path}:{it.line} -> Karmaşıklık yüksek ({it.code}). "
                "Fonksiyonu daha küçük parçalara bölmeyi, erken dönüş (early return) "
                "ve yardımcı fonksiyonlar kullanmayı düşün."
            )

        # Pylint klasik kurallar
        if it.tool == "pylint":
            if it.code in {"R0912", "R0914", "R0915"}:
                suggestions.append(
                    f"{it.path}:{it.line} -> {it.code} (çok fazla dal/parametre/durum). "
                    "Fonksiyonu sadeleştir, yardımcı fonksiyonlara ayır."
                )
            if it.code == "C0103":
                suggestions.append(
                    f"{it.path}:{it.line} -> {it.code} (isimlendirme kuralı). "
                    "PEP8'e uygun, daha açıklayıcı isimler kullan."
                )
            if it.code.startswith(("E", "F")):
                suggestions.append(
                    f"{it.path}:{it.line} -> {it.code} (hata/çıktı). Önce bu hatayı düzelt."
                )

        # Flake8 basit örnekler + ek boşluk önerileri
        if it.tool == "flake8":
            if it.code == "E302":
                suggestions.append(
                    f"{it.path}:{it.line} -> E302 (2 boş satır gerekli). "
                    "Fonksiyon/sınıf tanımlarından önce iki boş satır bırak."
                )
            if it.code == "E501":
                suggestions.append(
                    f"{it.path}:{it.line} -> E501 (satır çok uzun). "
                    "Uzun satırları böl (ör. parantez içi satır kırma)."
                )
            if it.code in {"E225", "E226", "E227"}:
                suggestions.append(
                    f"{it.path}:{it.line} -> {it.code} (operatör çevresinde boşluk). "
                    "İkili operatörlerin etrafına birer boşluk koy (örn. a + b, i % 2)."
                )
            if it.code == "E231":
                suggestions.append(
                    f"{it.path}:{it.line} -> E231 (ayraçtan sonra boşluk). "
                    "Virgül veya iki nokta sonrasında bir boşluk bırak (örn. f(x, y))."
                )
            if it.code == "E228":
                suggestions.append(
                    f"{it.path}:{it.line} -> E228 (modulo etrafında boşluk). "
                    "% operatörünün iki yanına boşluk ekle (örn. i % 2)."
                )

    # Tekilleştir ve sırala
    return sorted(set(suggestions))
