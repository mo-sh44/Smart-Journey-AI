# Projektstand und offene technische Fragen

## 1. Aktueller Stand

Smart Journey AI ist aktuell ein lauffaehiger MVP-Prototyp mit:

- Streamlit-Oberflaeche
- Local AI mode fuer KI-generierte Reisevorschlaege
- Demo mode fuer eine stabile Live-Demo
- echter Wetter-API ueber Visual Crossing
- vorbereitetem OpenAI Assistant
- Tool-Calling-Struktur ueber `ToolDispatcher`
- modularen Services fuer Wetter, Flug, Hotel, Kalender, E-Mail und BlueSky
- dokumentierter API-Risikoanalyse
- sicheren Einzeltests fuer externe Datenquellen

Der aktuelle MVP fokussiert sich auf wetterbasierte Reiseplanung mit KI-generierter Antwort im Local AI mode. Der Demo mode bleibt als stabiler Fallback erhalten. Flug- und Hoteldaten wurden technisch geprueft, sind aber aktuell nicht stabil genug fuer eine verlaessliche Live-Demo.

## 2. Vorfuehrbare Funktionen

### App starten

```powershell
cd C:\Users\PC\Documents\Codex\SmartJourneyAI_Compare
.\.venv\Scripts\Activate.ps1
python -m streamlit run src/main.py
```

In der App:

```text
Mode: Local AI
```

Beispielanfrage:

```text
Ich plane eine Reise von Berlin nach Barcelona vom 10.07.2026 bis 14.07.2026. Bitte pruefe das Wetter und erstelle einen kurzen Reisevorschlag.
```

### Sichere Testuebersicht

```powershell
python src/test_apis.py
```

Diese Datei fuehrt keine riskanten Aktionen aus. Sie zeigt nur die verfuegbaren Einzeltests.

## 3. API-Tests

### Wetter-API

```powershell
python src/test_weather_api.py
```

Aktuelles Ergebnis:

- funktioniert
- liefert echte Wetterdaten fuer Barcelona
- ist fuer den MVP geeignet

Bewertung:

```text
Die Wetter-API ist aktuell die stabilste Live-Datenquelle im Projekt.
```

### Flugquelle

```powershell
python src/test_flight_source.py
```

Aktuelles Ergebnis:

```text
No flights found for this route.
```

Risiko:

- Die aktuelle Flugquelle nutzt Swoodoo-Scraping.
- Die Webseite liefert zwar HTML, aber die erwarteten Flugdaten koennen nicht verlaesslich extrahiert werden.
- CSS-Klassen und HTML-Strukturen koennen sich aendern.
- Scraping kann durch Webseiten blockiert werden.

Alternative:

- Fuer die Zwischenpraesentation Flug-Live-Daten nicht als kritischen MVP-Teil verwenden.
- Flugoptionen bei Bedarf als Beispiel-/Fallback-Daten zeigen.
- Fuer die Endpraesentation offizielle Flug-APIs pruefen, z.B. Skyscanner Partner API, Amadeus oder andere Anbieter.

Offene Frage:

```text
Ist es fuer die Zwischenpraesentation akzeptabel, Flugoptionen als Fallback-Daten zu behandeln, wenn die Live-Quelle ueber Scraping nicht stabil ist?
```

### Hotelquelle

```powershell
python src/test_hotel_source.py
```

Aktuelles Ergebnis:

```text
Hotel search failed (HTTP 202).
```

Risiko:

- Die aktuelle Hotelquelle nutzt Booking.com-Scraping.
- HTTP 202 liefert keine direkt verwertbaren Hotelkarten.
- Booking.com kann Inhalte dynamisch nachladen oder automatisierte Requests einschranken.
- Scraping ist fuer eine stabile Live-Demo nicht verlaesslich genug.

Alternative:

- Fuer die Zwischenpraesentation Hotel-Live-Daten nicht als kritischen MVP-Teil verwenden.
- Hoteloptionen bei Bedarf als Beispiel-/Fallback-Daten zeigen.
- Fuer die Endpraesentation offizielle Hotel- oder Content-APIs pruefen, z.B. Amadeus Hotel API oder TripAdvisor Content API.

Offene Frage:

```text
Soll der Hotelteil bis zur Endpraesentation zwingend mit echten Live-Daten umgesetzt werden, oder sind Fallback-Daten mit dokumentierter API-Risikoanalyse ausreichend?
```

### BlueSky

```powershell
python src/test_bluesky_source.py
```

Aktueller Stand:

- BlueSky-Service ist vorbereitet.
- Der sichere Test liest nur letzte Posts.
- Es wird nichts veroeffentlicht.
- Zugangsdaten muessen lokal in `.env` gesetzt werden.

Risiko:

- Fuer BlueSky werden echte Zugangsdaten benoetigt.
- Versehentliches Posten soll vermieden werden.
- Deshalb wird aktuell nur ein Read-Test verwendet.

Alternative:

- BlueSky zuerst nur fuer Personalisierung nutzen.
- Veröffentlichen erst spaeter und nur nach expliziter Nutzerbestaetigung.
- App-Passwort statt normales Passwort verwenden.

Offene Frage:

```text
Reicht fuer die Zwischenpraesentation ein sicherer BlueSky-Read-Test als Nachweis der technischen Machbarkeit?
```

### OpenAI Assistant

Aktueller Stand:

- Assistant Setup wurde vorbereitet.
- Thread/Assistant IDs koennen in `.env` gespeichert werden.
- Tool Calling ist im Code vorgesehen.

Risiko:

- OpenAI API-Nutzung ist getrennt von ChatGPT Plus/Pro.
- Ohne API-Billing oder ausreichendes Quota kann der Live-Run fehlschlagen.
- Die Assistants API ist langfristig abgeloest bzw. migrationsbeduerftig.

Alternative:

- Local AI mode als KI-Demo ohne OpenAI-Kosten.
- Demo mode als stabiler Fallback ohne LLM.
- OpenAI Assistant als Architektur- und Tool-Calling-Komponente erklaeren.
- Fuer die Endpraesentation ggf. API-Budget klaeren oder auf neuere OpenAI-Struktur migrieren.

Offene Frage:

```text
Ist es fuer die Zwischenpraesentation ausreichend, den OpenAI Assistant eingerichtet und die Agentenlogik erklaerbar zu haben, wenn der Live-Run wegen API-Quota/Billing nicht verlaesslich ist?
```

## 4. MVP-Entscheidung

Der aktuelle MVP wird bewusst stabil gehalten:

- Wetterdaten live
- Reisevorschlag live in der App
- KI-generierte Antwort ueber Local AI mode
- Flug/Hotel als dokumentierte Risikoquellen
- Demo mode als technische Fallback-Variante
- OpenAI Assistant als vorbereitete Agentenkomponente

Begruendung:

```text
Die technische Pruefung hat gezeigt, dass nicht alle Datenquellen gleich verlaesslich sind.
Deshalb wird der MVP auf die stabilen Bestandteile fokussiert und riskante Quellen werden transparent dokumentiert.
```

## 5. Geplante Erweiterungen

Fuer die naechste Projektphase:

- BlueSky Read-Test mit App-Passwort durchfuehren
- Local AI mode mit Ollama/Gemma lokal testen
- BlueSky-Posts fuer Personalisierung nutzen
- Google Calendar mit echten OAuth-Credentials testen
- E-Mail/ICS kontrolliert mit Testempfaenger pruefen
- Flug- und Hotel-Fallback-Daten in der App sichtbarer machen
- offizielle APIs fuer Flug und Hotel recherchieren
- OpenAI Assistant Live-Modus nur mit gesichertem API-Budget testen
- Fehlerbehandlung in der UI weiter verbessern

## 6. Fragen zur Scope-Abstimmung

1. Reicht fuer die Zwischenpraesentation ein stabiler MVP mit echter Wetter-API, Local AI mode und dokumentierten Risiken fuer Flug/Hotel?
2. Werden echte Live-Flug- und Live-Hoteldaten fuer die Zwischenpraesentation erwartet?
3. Falls Flug/Hotel-Live-Daten nicht stabil verfuegbar sind: Sind Fallback-Daten fuer die Demo akzeptabel?
4. Soll der Fokus eher auf Agentenlogik und Tool Calling liegen oder auf moeglichst vielen angebundenen Datenquellen?
5. Reicht BlueSky als Read-Test fuer Personalisierung, oder soll auch das Veröffentlichen eines Posts gezeigt werden?
6. Soll Google Calendar bis zur Zwischenpraesentation live gezeigt werden oder reicht die vorbereitete Architektur?
7. Ist die aktuelle MVP-Anpassung fachlich passend fuer den weiteren Projektverlauf?

## 7. Kurzfassung

```text
Smart Journey AI ist aktuell ein lauffaehiger MVP-Prototyp.
Die Wetter-API funktioniert live und stabil.
Der Local AI mode ist als KI-Demo ohne OpenAI-Kosten vorbereitet.
Flug- und Hoteldaten wurden getestet, sind ueber Scraping aber nicht verlaesslich genug.
Der MVP wurde deshalb auf stabile wetterbasierte Reiseplanung fokussiert.
Weitere Integrationen sind vorbereitet und werden nach Machbarkeit priorisiert.
```
