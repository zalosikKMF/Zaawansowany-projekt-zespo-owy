"""Klasyfikacja jakosci powietrza na podstawie PM2.5 (ug/m3) - skala uproszczona WHO/EU."""


def pm25_quality(pm25: float | None) -> tuple[str, str]:
    if pm25 is None:
        return "brak danych", "#94a3b8"
    if pm25 <= 10:
        return "bardzo dobry", "#22c55e"
    if pm25 <= 20:
        return "dobry", "#84cc16"
    if pm25 <= 25:
        return "umiarkowany", "#eab308"
    if pm25 <= 50:
        return "dostateczny", "#f97316"
    if pm25 <= 75:
        return "zly", "#ef4444"
    return "bardzo zly", "#7f1d1d"


def quality_bucket(pm25: float | None) -> str:
    label, _ = pm25_quality(pm25)
    return label
