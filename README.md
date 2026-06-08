# Smart Journey AI - Reiseplanung mit KI

Smart Journey AI ist ein KI-gestuetzter Reiseassistent fuer die Projektarbeit an der HTW Berlin. Das System soll nicht nur Fragen beantworten, sondern Reiseplanungsschritte automatisieren: Nutzereingabe analysieren, Wetterdaten abrufen, externe Datenquellen pruefen, Ergebnisse bewerten und daraus einen Reisevorschlag erstellen.

Der aktuelle Zwischenstand ist ein MVP-Prototyp. Er nutzt echte Wetterdaten und dokumentiert technische Risiken bei Flug- und Hoteldaten.

## Projektziel

Der Nutzer beschreibt eine Reiseidee, z.B.:

```text
Ich plane eine Reise von Berlin nach Barcelona vom 10.07.2026 bis 14.07.2026. Bitte pruefe das Wetter und erstelle einen kurzen Reisevorschlag.
```

Smart Journey AI soll daraus:

- Reiseziel und Zeitraum erkennen
- Wetterdaten fuer das Reiseziel abrufen
- einen ersten Reisevorschlag erstellen
- spaeter Flug-, Hotel-, Kalender-, E-Mail- und BlueSky-Funktionen anbinden

## Aktueller Stand

Dieser Stand ist fuer die Review-Session mit dem Dozenten vorbereitet. Ziel ist zu zeigen, dass nicht nur die Idee existiert, sondern bereits ein lauffaehiger MVP, praktische API-Tests und eine begruendete Risikoanalyse vorhanden sind.

Bereits umgesetzt:

- Streamlit-App mit heller, gut lesbarer Oberflaeche
- Demo mode ohne OpenAI-Kosten
- echte Wetter-API ueber Visual Crossing
- OpenAI Assistant wurde eingerichtet
- Flugquelle wurde getestet, aber als instabil bewertet
- Hotelquelle wurde getestet, aber als instabil bewertet
- BlueSky-Service ist vorbereitet und kann letzte Posts abrufen
- API-Testlog und MVP-Plan dokumentiert

Der MVP ist bewusst angepasst:

```text
Wetterdaten sind live.
Flug- und Hoteldaten werden vorerst als Risiko dokumentiert.
OpenAI Assistant ist eingerichtet, aber bei API-Quota/Billing kann Demo mode genutzt werden.
```

## Geplante Erweiterungen

Fuer die Endpraesentation sind diese Erweiterungen geplant:

- stabilere Flugquelle ueber offizielle API statt Swoodoo-Scraping
- stabilere Hotelquelle ueber offizielle API statt Booking.com-Scraping
- Google-Calendar-Test mit echten freien Zeitraeumen
- BlueSky-Personalisierung durch Analyse der letzten Posts
- optionale BlueSky-Veröffentlichung nach Nutzerbestätigung
- E-Mail-Versand mit Kalenderdatei nach finaler Auswahl
- bessere Fehlerbehandlung fuer alle externen APIs
- klarere Trennung zwischen Live-Daten und Fallback-Daten

## Projektstruktur

```text
smart-journey-ai/
  data/
    user_profile.pdf
    credentials.json          # lokal, nicht auf GitHub
  docs/
    API_MVP_Plan.md
    API_Testlog.md
  src/
    main.py                   # Streamlit App
    core/
      assistant_setup.py      # OpenAI Assistant einrichten
      openai_handler.py       # OpenAI Thread/Run/Tool-Calls
      tool_dispatcher.py      # Weiterleitung von Tool Calls an Services
      demo_mode.py            # stabiler MVP-Demo-Modus
    services/
      weather_service.py
      flight_service.py
      hotel_service.py
      calendar_service.py
      email_service.py
      bluesky_service.py
    test_weather_api.py
    test_flight_source.py
    test_hotel_source.py
  .env.example
  requirements.txt
```

## Einrichtung

### 1. In den Projektordner wechseln

```powershell
cd C:\Users\PC\Documents\Codex\SmartJourneyAI_Compare
```

### 2. Virtuelle Umgebung aktivieren

Wenn im Gruppenrepo eine eigene `.venv` existiert:

```powershell
.\.venv\Scripts\Activate.ps1
```

Falls noch keine `.venv` existiert:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. `.env` vorbereiten

```powershell
copy .env.example .env
```

Dann `.env` lokal ausfuellen:

```env
OPENAI_API_KEY=
ASSISTANT_ID=
THREAD_ID=
VISUAL_CROSSING_API_KEY=
BLUESKY_USERNAME=
BLUESKY_PASSWORD=
GOOGLE_CREDENTIALS_PATH=./data/credentials.json
SMTP_SERVER=
SMTP_PORT=587
SMTP_SENDER=
SMTP_PASSWORD=
```

Wichtig:

```text
.env niemals committen.
data/credentials.json niemals committen.
```

## API-Tests

### Wetter-API testen

```powershell
python src/test_weather_api.py
```

Erwartetes Ergebnis:

```text
Weather API works.
2026-07-10: 23.8 C - 25.2 C, Partially cloudy
...
```

Bewertung:

```text
Die Wetter-API funktioniert und ist fuer den MVP geeignet.
```

### Flugquelle testen

```powershell
python src/test_flight_source.py
```

Aktuelles Ergebnis:

```text
No flights found for this route.
```

Bewertung:

```text
Swoodoo wird ueber Scraping abgefragt.
Im Test konnten keine verlaesslichen Flugdaten extrahiert werden.
Fuer die Zwischenpraesentation wird Flug-Live-Datenzugriff nicht als kritischer MVP-Teil verwendet.
```

### Hotelquelle testen

```powershell
python src/test_hotel_source.py
```

Aktuelles Ergebnis:

```text
Hotel search failed (HTTP 202).
```

Bewertung:

```text
Booking.com wird ueber Scraping abgefragt.
HTTP 202 liefert keine direkt verwertbaren Hotelkarten.
Fuer die Zwischenpraesentation wird Hotel-Live-Datenzugriff nicht als kritischer MVP-Teil verwendet.
```

### BlueSky-Quelle testen

Vorher `.env` ausfuellen:

```env
BLUESKY_USERNAME=
BLUESKY_PASSWORD=
```

Dann ausfuehren:

```powershell
python src/test_bluesky_source.py
```

Erwartetes Ergebnis:

```text
BlueSky source works.
Fetched posts: 3
```

Bewertung:

```text
BlueSky kann fuer Personalisierung genutzt werden, wenn Zugangsdaten vorhanden sind.
Der sichere Test liest nur Posts und veroeffentlicht nichts.
```

## App starten

```powershell
python -m streamlit run src/main.py
```

Dann im Browser oeffnen:

```text
http://localhost:8501
```

Fuer die Zwischenpraesentation links in der Sidebar auswaehlen:

```text
Demo mode
```

Beispiel-Prompt:

```text
Ich plane eine Reise von Berlin nach Barcelona vom 10.07.2026 bis 14.07.2026. Bitte pruefe das Wetter und erstelle einen kurzen Reisevorschlag.
```

Weitere Quickstarts im Demo mode:

```text
City break in Europe this summer
Plan a beach holiday next month
Winter trip to the Alps
```

Diese Quickstarts erzeugen unterschiedliche Demo-Szenarien.

## OpenAI Assistant einrichten

Wenn ein gueltiger OpenAI API-Key mit API-Budget vorhanden ist:

```powershell
python src/core/assistant_setup.py
```

Das Skript erstellt:

- OpenAI Assistant
- Conversation Thread
- optional File Search / Vector Store mit Nutzerprofil
- `ASSISTANT_ID`
- `THREAD_ID`

Die IDs werden automatisch in `.env` gespeichert.

Falls bei der App im OpenAI Assistant mode diese Meldung kommt:

```text
You exceeded your current quota
```

dann liegt es nicht am Code, sondern an OpenAI API-Billing/Quota.

## BlueSky-Integration

Der Kollege hat BlueSky als Service vorbereitet:

```text
src/services/bluesky_service.py
```

Funktionen:

- `fetch_recent_posts(limit=25)`
  - loggt sich bei BlueSky ein
  - liest die letzten Posts des Accounts
  - speichert sie lokal in `data/social_posts.json`

- `publish_post(text)`
  - erstellt eine BlueSky-Session
  - veroeffentlicht einen neuen Post

Sicherer Einzeltest:

```powershell
python src/test_bluesky_source.py
```

BlueSky wird auch im alten Komplett-Test angesprochen:

```powershell
python src/test_apis.py
```

Aber Vorsicht:

```text
test_apis.py testet auch E-Mail und Google Calendar.
Das kann echte Aktionen ausloesen.
Fuer die Zwischenpraesentation lieber einzelne sichere Tests verwenden.
```

Sicherer BlueSky-Test waere:

```python
from services.bluesky_service import BlueskyService

posts = BlueskyService().fetch_recent_posts(limit=3)
print(posts)
```

Voraussetzung:

```env
BLUESKY_USERNAME=
BLUESKY_PASSWORD=
```

Am besten ein BlueSky-App-Passwort verwenden, nicht das normale Passwort.

## Dokumentation

Wichtige Dateien:

```text
docs/API_Testlog.md
docs/API_MVP_Plan.md
```

`API_Testlog.md` dokumentiert:

- Wetter-API funktioniert
- OpenAI Assistant wurde eingerichtet
- Flugquelle wurde getestet, aber ist instabil
- Hotelquelle wurde getestet, aber ist instabil
- Demo mode wurde umgesetzt

`API_MVP_Plan.md` dokumentiert:

- MVP-Entscheidung
- API-Risiken
- Scope-Anpassung fuer Zwischenpraesentation
- naechste Schritte fuer Endpraesentation

## Formulierung fuer die Zwischenpraesentation

```text
Wir haben mehrere Datenquellen praktisch getestet.
Die Wetter-API funktioniert stabil und wird im MVP live verwendet.
Flug- und Hoteldaten wurden ueber Scraping getestet, lieferten aber keine verlaesslich strukturierten Ergebnisse.
Deshalb wurde der MVP angepasst: Die Zwischenpraesentation zeigt eine stabile Reiseplanung mit echter Wetter-API und dokumentiert Flug/Hotel als technische Risiken fuer die naechste Phase.
```

## Git-Sicherheit

Nicht committen:

```text
.env
data/credentials.json
data/token.json
data/social_posts.json
.venv/
```

Pruefen:

```powershell
git status --short
```

Commit:

```powershell
git add .
git commit -m "Describe your change"
```

Push:

```powershell
git push origin Feroza
```
