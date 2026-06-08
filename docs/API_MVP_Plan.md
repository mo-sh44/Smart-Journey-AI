# Smart Journey AI - API- und MVP-Plan

## Projektanforderungen

Der naechste Projektstand soll zeigen, dass die technische Machbarkeit praktisch geprueft wurde. Besonders wichtig sind:

1. APIs recherchieren und testen
2. dokumentieren, was funktioniert und was nicht
3. frueh einen Prototypen entwickeln
4. technische Risiken analysieren
5. Projektidee bei Bedarf anpassen

## Empfohlene Reihenfolge

Fuer die Zwischenpraesentation sollten wir nicht versuchen, alle Funktionen perfekt fertigzustellen. Wichtiger ist ein stabiler, erklaerbarer MVP.

Prioritaet:

1. Streamlit-App starten
2. Wetter-API testen
3. OpenAI Assistant / Tool Calling einrichten
4. einfache Demo: Nutzer fragt nach Reise, Assistant ruft Wetterfunktion auf
5. Flug- und Hotelquellen testen und Risiken dokumentieren
6. MVP-Grenzen definieren

## MVP fuer die Zwischenpraesentation

Der MVP soll zeigen:

- Eine einfache Streamlit-Oberflaeche ist vorhanden.
- Der Nutzer kann eine Reiseanfrage stellen.
- Der Assistant kann mindestens ein echtes Tool nutzen.
- Die Wetter-API liefert reale Daten.
- Das System erzeugt daraus einen ersten Reisevorschlag.
- API-Risiken fuer Flug, Hotel und Bewertungsdaten sind dokumentiert.

Noch nicht zwingend notwendig fuer die Zwischenpraesentation:

- vollstaendige Buchungslogik
- echte Flugbuchung
- echte Hotelbuchung
- perfekte UI
- vollstaendige Kalender- und E-Mail-Automatisierung

## API-Analyse

### 1. OpenAI Assistant

Status: geplant / einzurichten

Zweck:

- zentrale Agentenlogik
- Analyse der Nutzeranfrage
- Entscheidung, welche Tools aufgerufen werden
- Kombination der Tool-Ergebnisse zu einer Antwort

Risiko:

- API-Versionen und Modelle koennen sich aendern.
- Das bestehende Projekt nutzt eine aeltere Assistant-Struktur.

MVP-Entscheidung:

- Fuer den Zwischenstand nutzen wir die bestehende Assistant-Struktur.
- Spaeter kann modernisiert werden, falls noetig.

### 2. Wetter-API

Status: hoechste Prioritaet

Geplante Datenquelle:

- Visual Crossing Weather API

Zweck:

- Wetter fuer Zielort und Reisezeitraum abrufen
- Reiseempfehlung wetterabhaengig begruenden

Warum gut fuer MVP:

- klar testbar
- gut erklaerbar
- passt direkt zur Anforderung, APIs frueh praktisch zu testen

Erfolgskriterium:

- Beispielanfrage wie Berlin, Paris oder Barcelona liefert strukturierte Wetterdaten.

### 3. Flugdaten

Status: getestet, riskant

Aktueller Projektstand:

- Swoodoo wird ueber HTML-Scraping abgefragt.

Problem:

- Webseiten koennen Scraping blockieren.
- HTML-Strukturen koennen sich aendern.
- Ergebnisse sind nicht garantiert stabil.

Alternative:

- Skyscanner bietet offizielle Flight APIs, aber der Zugang ist eher fuer Partner gedacht und muss geprueft bzw. beantragt werden.

MVP-Entscheidung:

- Der Swoodoo-Test lieferte keine verwertbaren Flugdaten.
- Fuer die Zwischenpraesentation werden Flug-Live-Daten nicht als kritischer Bestandteil verwendet.
- Falls Flugoptionen gezeigt werden, werden Beispiel-/Mockdaten genutzt.

### 4. Hoteldaten

Status: getestet, riskant

Aktueller Projektstand:

- Booking.com wird ueber HTML-Scraping abgefragt.

Problem:

- Scraping ist instabil.
- Seiten koennen blockieren oder andere HTML-Strukturen ausliefern.

Alternative:

- TripAdvisor Content API ist moeglich, aber zugangsbeschraenkt und nicht garantiert sofort nutzbar.

MVP-Entscheidung:

- Der Booking.com-Test lieferte HTTP 202 und keine direkt verwertbaren Hotelkarten.
- Fuer die Zwischenpraesentation werden Hotel-Live-Daten nicht als kritischer Bestandteil verwendet.
- Falls Hoteloptionen gezeigt werden, werden Beispiel-/Mockdaten genutzt.

### 5. TripAdvisor / Bewertungsdaten

Status: zu pruefen

Zweck:

- Aktivitaeten, Sehenswuerdigkeiten oder Bewertungen einbinden

Problem:

- API-Zugang ist eingeschraenkt.
- Nicht sicher, ob eine schnelle Freigabe fuer ein Hochschulprojekt moeglich ist.

MVP-Entscheidung:

- Fuer den Zwischenstand nur als recherchierte Option dokumentieren.
- Nicht als kritische Funktion fuer die Demo einplanen.

## Demo-Idee fuer die Zwischenpraesentation

Beispielablauf:

1. App im Browser starten
2. Kurze Reiseanfrage eingeben:

```text
Ich moechte im Juli fuer 5 Tage nach Barcelona reisen. Bitte pruefe das Wetter und schlage mir eine passende Reiseplanung vor.
```

3. Assistant erkennt: Wetterdaten werden benoetigt
4. Wetterfunktion wird ausgefuehrt
5. Ergebnis wird in einen einfachen Reisevorschlag eingebaut

Falls OpenAI Assistant live noch nicht stabil ist:

- Wetter-API separat live zeigen
- App-Oberflaeche zeigen
- Agentenablauf mit Diagramm oder Pseudocode erklaeren

## Anpassung der Projektidee

Falls Flug- und Hotel-APIs nicht stabil verfuegbar sind, wird das Projekt fuer den MVP spezialisiert:

**Smart Journey AI als personalisierter Reiseplanungsassistent mit Wetter-, Kalender- und Interessenanalyse.**

Flug und Hotel werden dann als:

- Beispieloptionen
- Mockdaten
- spaeter erweiterbare Schnittstellen

behandelt.

Das ist keine Schwaeche, sondern eine realistische Scope-Anpassung.
