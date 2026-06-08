# Review Session Checklist

Diese Checkliste ist fuer den Termin mit dem Dozenten vor der Zwischenpraesentation.

## 1. Projekt vorbereiten

Im Terminal:

```powershell
cd C:\Users\PC\Documents\Codex\SmartJourneyAI_Compare
.\.venv\Scripts\Activate.ps1
git status --short
```

Erwartung:

```text
git status --short sollte leer sein.
```

## 2. Sichere Testuebersicht zeigen

```powershell
python src/test_apis.py
```

Erklaerung:

```text
Wir haben den alten Kompletttest entschaerft, weil einige Integrationen echte Aktionen ausloesen koennen.
Stattdessen nutzen wir kontrollierte Einzeltests.
```

## 3. Wetter-API live testen

```powershell
python src/test_weather_api.py
```

Erklaerung:

```text
Die Wetter-API funktioniert stabil und liefert echte Wetterdaten fuer das Reiseziel.
Diese API ist deshalb Teil unseres MVP.
```

## 4. Flugquelle testen

```powershell
python src/test_flight_source.py
```

Erklaerung:

```text
Die Flugquelle wurde getestet, liefert aber keine verlaesslichen strukturierten Daten.
Der Grund ist, dass aktuell Swoodoo-Scraping genutzt wird.
Fuer den MVP verwenden wir Flug-Live-Daten deshalb nicht als kritischen Bestandteil.
```

## 5. Hotelquelle testen

```powershell
python src/test_hotel_source.py
```

Erklaerung:

```text
Die Hotelquelle wurde getestet, antwortet aber mit HTTP 202 und liefert keine direkt verwertbaren Hotelkarten.
Auch hier ist Scraping ein technisches Risiko.
```

## 6. App starten

```powershell
python -m streamlit run src/main.py
```

Dann im Browser:

```text
http://localhost:8501
```

In der Sidebar auswaehlen:

```text
Demo mode
```

Demo-Prompt:

```text
Ich plane eine Reise von Berlin nach Barcelona vom 10.07.2026 bis 14.07.2026. Bitte pruefe das Wetter und erstelle einen kurzen Reisevorschlag.
```

## 7. BlueSky erwaehnen

Wenn BlueSky-Zugangsdaten in `.env` vorhanden sind:

```powershell
python src/test_bluesky_source.py
```

Wenn keine Zugangsdaten vorhanden sind:

```text
BlueSky ist als Service vorbereitet.
Der sichere Test liest nur letzte Posts und veroeffentlicht nichts.
Live-Test erfolgt erst mit App-Passwort.
```

## 8. Wichtigste Aussage fuer den Dozenten

```text
Wir haben mehrere Datenquellen praktisch getestet.
Wetter funktioniert stabil ueber eine echte API.
Flug und Hotel wurden getestet, sind aber ueber Scraping nicht stabil genug.
Deshalb haben wir den MVP angepasst: Die Zwischenpraesentation zeigt eine stabile Reiseplanung mit echter Wetter-API und dokumentierten API-Risiken.
```

## 9. Aktueller Stand in einem Satz

```text
Smart Journey AI ist aktuell ein lauffaehiger MVP-Prototyp mit Streamlit-Oberflaeche, echter Wetter-API, vorbereitetem OpenAI Assistant, dokumentierter API-Risikoanalyse und sicherem Demo-Modus.
```

