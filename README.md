# Schach-API
Deutsche Schach-API für Python

## 📋 Inhaltsverzeichnis
- [Verfügbare Funktionen](#verfügbare-funktionen)
- [Anleitung](#anleitung)
- [Wichtige Hinweise](#wichtige-hinweise)
- [Variableninfo](#variableninfo)
- [Technische Details](#technische-details)

## Verfügbare Funktionen
- **visual_feldname**
    Visualisiert die Feldnummer als Schachfeldname
- **visual_farbe**
    Visualisiert die Farbnummer als Farbnamen
- **visual_farbenkürzel**
    Visualisiert die Farbnummer als Farbkürzel
- **visual_figur**
    Visualisiert die Figurnummer als Figurennamen
- **visual_figurkürzel**
    Visualisiert die Figurnummer als Figurenkürzel
- **tec_feldfarbe**
    Gibt die technische Feldfarbe der angegebenen Feldnummer zurück
- **neues_spiel**
    Erstellt die Variablen für ein neues Spiel
- **fstatus_func**
    Erstellt die Statusvariable - Sortierung: Farbe > Figur >> Felder
- **farbe_figur_auf_feld**
    Gibt die Armeefarbe und Figur auf dem übermittelten Feld aus
- **figurfelder_final**
    Kompiliert die allgemein möglichen Figurfelder der Figur auf dem entsprechenden Startfeld unter Berücksichtigung von Minenfeldern, Fesselungen und Schachsituationen und gibt diese Liste aus.
- **armeefiguren_final**
    Gibt final für die übergebene Farbe die Liste der bewegungsfähigen Figuren anhand deren Felder aus. Alle relevanten Funktionen werden dabei berücksichtigt.
- **zug_final**
    Führt den angegebenen Zug aus, aktualisiert `kstatus`, `ep`, `roch` und gibt zusätzlich die Umwandlung, Schachangriff, Schachmatt und Unentschieden (Patt) als boolesche Werte zurück.
- **figur_umwandlung**
    Konvertiert die Figur auf dem angegebenen Feld in die angegebene Figur (zulässig 1-6). Kann für Umwandlungen verwendet werden.

## Anleitung

1. **Spielstart:**
   Zum Spielstart müssen 3 Variablen lokal angelegt werden mit der Funktion `neues_spiel()`:
   ```python
   kstatus, roch, ep = schach_api.neues_spiel()
   ```

2. **Spielfeldvisualisierung:**
   `kstatus` ist ein Dictionary, das von den Figuren ausgehend ihre besetzten Felder anzeigt. Mit der Funktion `fstatus_func()` kann daraus ein anderes Dictionary hergeleitet werden.

3. **Bei jedem Zug:**
   - Mit `armeefiguren_final()` erhältst du eine Liste der Figuren (nach ihren Feldern), die ziehen können und dürfen.
   - Mit `figurfelder_final()` erhältst du eine Liste, welche Felder die ausgewählte Figur besetzen kann und darf.
   - Mit `zug_final()` setzt du den `kstatus` neu anhand der angegebenen Figurbewegung.

4. **Sonderfälle:**
   `zug_final()` gibt zusätzliche Informationen aus:
   - **Umwandlung:**
     Mit `figur_umwandlung()` setzt du den `kstatus` neu anhand der angegebenen Figurkonvertierung.
   - **Schach:**
     Wenn die gezogene Farbe den gegnerischen König angreift.
   - **Schachmatt:**
     Wenn die gezogene Farbe den gegnerischen König angreift und das Gegnerteam keinen Verteidigungszug ausführen kann.
   - **Patt:**
     Wenn die gezogene Farbe den gegnerischen König nicht angreift, aber das Gegnerteam keinen Zug mehr ausführen kann.

## ⚠️ Wichtige Hinweise
- Die Funktion `zug_final()` prüft keine validen Züge, deswegen ist ein korrektes Spiel nur gewährleistet, wenn die richtigen Werte ordentlich weitergereicht werden. 💎

## Variableninfo

- **ep**
  EnPassant-Felder, die aktuell gültig sind

- **roch**
  Rochade-Felder, die aktuell gültig sind

- **kstatus**
  Allgemeine Statusvariable - beinhaltet die Startsituation - Sortierung: Farbe > Figur >> Liste der Felder

## Technische Details

### Spielfeld
```
🔽 schwarz
18  28  38  48  58  68  78  88
17  27  37  47  57  67  77  87
16  26  36  46  56  66  76  86
15  25  35  45  55  65  75  85
14  24  34  44  54  64  74  84
13  23  33  43  53  63  73  83
12  22  32  42  52  62  72  82
11  21  31  41  51  61  71  81
🔼 weiß
```

### Farbe
- `< 10` = **w** / Weiß ⚪
- `< -10` = **s** / Schwarz ⚫
- `= 0` = leer

### Figuren
- `1` = **b** / Bauer
- `2` = **s** / Springer
- `3` = **l** / Läufer
- `4` = **t** / Turm
- `5` = **d** / Dame
- `6` = **k** / König