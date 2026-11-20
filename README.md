# OP-1 hundekraft – Kurzreferenz

Deutsche Kurzreferenz zur [hundekraft-Firmware 3.3.1](https://hundekraft.github.io/op1-workshop/) für die originale OP-1, als Web-App fürs iPhone.

- 91 Einträge: Synths, Drums, Effekte, Sequenzer, Tape, System und MIDI
- Schnellzugriffe mit Tastenweg, Encoder-Belegung in den vier Farben
- Suche (deutsch und Display-Begriffe), Favoriten, zuletzt angesehen
- Je Eintrag umschaltbar zwischen „Kurz“ und „Ausführlich“: der Handbuchtext auf Deutsch, mit den Tasten-Icons und Bildschirmfotos des Originals, Sprungleiste und Großansicht der Bilder
- Die Suche findet auch Stellen im ausführlichen Text
- Läuft nach dem ersten Laden ohne Netz (Service Worker), mit eigenem App-Icon; das Display bleibt an, solange ein Eintrag offen ist
- Kein Build-Schritt: `index.html` (App), `anleitung.js` (ausführliche Texte, wird erst beim Einschalten geladen), `manual/` (Bilder), `sw.js` und `manifest.webmanifest` (Offline-Betrieb, App-Icon)

## Benutzen

`index.html` im Browser öffnen. Auf dem iPhone in Safari über „Teilen → Zum Home-Bildschirm“ wie eine App ablegen. Favoriten werden nur lokal im Browser gespeichert.

Für GitHub Pages: Settings → Pages → Branch `main`, Ordner `/`.

## Inhalt und Herkunft

Die Kurzreferenz ist eine eigene, verdichtete Zusammenfassung. Die ausführliche Anleitung (`anleitung.js`) ist eine deutsche Übersetzung der passenden Abschnitte aus dem Handbuch des hundekraft-Projekts ([hundekraft/op1-workshop](https://github.com/hundekraft/op1-workshop), GPL-3.0-or-later); die Bilder in `manual/` stammen unverändert von dort. Nicht übersetzt sind die Kapitel zu Firmware-Bau, Fehlersuche und Plugin-Entwicklung; Verweise dorthin führen ins englische Original. Der Build lässt diese Plugins aus: bitcrush, blot, brassophone, dddd, father, grids, hollowsaint, juni, juni_chorus, nostromo, plate_o, ploc, steve, vapora.

Kein offizielles Produkt von Teenage Engineering oder des hundekraft-Projekts.

## Texte ändern

Die deutschen Abschnitte liegen einzeln in `tools/de/`. Nach einer Korrektur erzeugt `python3 tools/build.py .` die Datei `anleitung.js` neu; `python3 tools/check.py <id>` vergleicht die Struktur mit dem Original in `tools/src/`.

## Lizenz

GPL-3.0-or-later, siehe `LICENSE`.
