# Smart Journey AI - Architektur und Ablauf

## Systemarchitektur

```mermaid
flowchart TD
    A["Nutzer gibt Reiseanfrage ein"] --> B["Streamlit Frontend"]
    B --> C{"Modus"}
    C -->|Demo mode| D["Demo Mode"]
    C -->|OpenAI Assistant| E["OpenAI Assistant Handler"]

    D --> F["WeatherService"]
    F --> G["Visual Crossing Weather API"]
    G --> D
    D --> H["Reisevorschlag mit echten Wetterdaten"]

    E --> I["OpenAI Thread und Run"]
    I --> J{"Tool Call benoetigt?"}
    J -->|Ja| K["ToolDispatcher"]
    K --> F
    K --> L["FlightService"]
    K --> M["HotelService"]
    K --> N["CalendarService"]
    K --> O["BlueSkyService"]
    K --> P["EmailService"]
    J -->|Nein| Q["Assistant Antwort"]
    K --> I
    I --> Q
    Q --> B
    H --> B
```

## Pseudocode

```text
User schreibt Reiseanfrage
Streamlit zeigt Anfrage im Chat

wenn Demo mode aktiv:
    Reiseziel und Datum aus Text erkennen
    Wetterdaten fuer Reiseziel abrufen
    Reisevorschlag mit Wetterbewertung erzeugen
    Antwort im Chat anzeigen

wenn OpenAI Assistant aktiv:
    Nachricht an OpenAI Thread senden
    Assistant Run starten
    solange Run nicht fertig:
        Status pruefen
        wenn Tool Call angefordert:
            ToolDispatcher ruft passende Service-Funktion auf
            Ergebnis an Assistant zurueckgeben
    finale Assistant-Antwort im Chat anzeigen
```

## Aktueller MVP-Ablauf

```mermaid
flowchart LR
    A["Reiseanfrage: Berlin nach Barcelona"] --> B["Demo mode"]
    B --> C["Zielort und Zeitraum extrahieren"]
    C --> D["WeatherService"]
    D --> E["Visual Crossing API"]
    E --> F["Wetterdaten"]
    F --> G["Reisevorschlag"]
    G --> H["Anzeige in Streamlit"]
```

## Tool- und Datenquellen

| Bereich | Implementierung | Status |
|---|---|---|
| Wetter | Visual Crossing API | funktioniert live |
| OpenAI | Assistant API / Tool Calling | eingerichtet, Quota/Billing abhaengig |
| Flug | Swoodoo-Scraping | technisch vorhanden, aber instabil |
| Hotel | Booking.com-Scraping | technisch vorhanden, aber instabil |
| BlueSky | atproto / BlueSky API | vorbereitet, Read-Test sicher |
| Kalender | Google Calendar API | vorbereitet |
| E-Mail | SMTP + ICS | vorbereitet, nur kontrolliert testen |

## Einordnung

Der wichtigste Punkt ist nicht, dass alle externen Quellen perfekt funktionieren, sondern dass jede Quelle technisch geprueft und bewertet wurde. Fuer stabile Live-Demos wird aktuell die Wetter-API verwendet. Flug und Hotel sind als Services vorhanden, muessen fuer die Endpraesentation aber entweder ueber stabilere APIs oder ueber kontrollierte Fallback-Daten abgesichert werden.

