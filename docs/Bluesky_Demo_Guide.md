# BlueSky Demo Guide

## Rolle von BlueSky im Projekt

BlueSky wird in Smart Journey AI fuer zwei Funktionen genutzt:

1. **Personalisierung vor der Reise**
   - Der Assistent liest die letzten Posts eines Demo-Accounts.
   - Aus den Posts werden Interessen erkannt.
   - Diese Interessen beeinflussen die Reiseempfehlung.

2. **Optionaler Reise-Post nach der Planung**
   - Der Assistent erstellt einen kurzen BlueSky-Post zur geplanten Reise.
   - Veröffentlicht wird nur nach expliziter Bestaetigung.

Damit entspricht die Umsetzung dem Referenzprojekt:

- `fetch_recent_posts(limit=25)` entspricht dem alten `fetch_posts(25)`.
- `publish_post(text)` entspricht dem alten `send_post(text)`.
- Die Posts werden lokal gespeichert und beim Assistant-Setup fuer File Search hochgeladen.

## Warum ein Demo-Account sinnvoll ist

Fuer die Praesentation sollte kein privater Account genutzt werden.
Ein Demo-Account ist besser, weil:

- keine privaten Daten gezeigt werden
- harmlose Beispiel-Posts vorbereitet werden koennen
- ein echter BlueSky-Login und echte API-Abfragen demonstriert werden
- optional ein echter Post veroeffentlicht werden kann

## Beispiel-Posts fuer den Demo-Account

Diese Posts koennen manuell im Demo-Account erstellt werden:

```text
Ich liebe mediterranes Essen, kleine Cafes und lokale Maerkte. Auf Reisen suche ich gern authentische Restaurants.
```

```text
Museen, Architektur und historische Stadtviertel interessieren mich besonders. Ich plane Reisen gern mit Kulturprogramm.
```

```text
Ich fotografiere gern schoene Strassen, Aussichtspunkte und Sonnenuntergaenge. Gute Fotospots sind mir wichtig.
```

```text
Ich mag warme Reiseziele, aber extreme Hitze ist fuer Sightseeing eher unpraktisch.
```

```text
Bei Staedtereisen brauche ich eine Mischung aus Kultur, Cafes, entspannten Spaziergaengen und gut erreichbaren Hotels.
```

## Sichere Tests

### 1. BlueSky-Posts lesen

```powershell
python src/test_bluesky_source.py
```

Dieser Test liest nur Posts und speichert sie in:

```text
data/social_posts.json
```

### 2. Personalisierung zeigen

```powershell
python src/test_bluesky_personalization.py
```

Dieser Test zeigt:

- wie viele Posts gelesen wurden
- welche Interessen erkannt wurden
- wie diese Interessen eine Barcelona-Reise beeinflussen

### 3. Post nur vorbereiten

```powershell
python src/test_bluesky_publish.py
```

Dieser Test zeigt nur den vorbereiteten Post.
Es wird nichts veroeffentlicht.

### 4. Post wirklich veroeffentlichen

Nur fuer einen Demo-Account verwenden:

```powershell
python src/test_bluesky_publish.py --publish
```

## Beispiel-Erklaerung fuer die Praesentation

```text
BlueSky dient bei uns als Social-Media-Kontext fuer Personalisierung.
Wir lesen die letzten Posts eines Demo-Accounts und erkennen daraus Interessen wie Kultur, Cafes, lokales Essen oder Fotospots.
Diese Interessen werden dann bei der Reiseplanung beruecksichtigt.
Nach der Planung kann der Assistent auch einen kurzen Reise-Post vorbereiten.
Veröffentlicht wird aber nur nach expliziter Bestaetigung.
```
