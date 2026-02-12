# Schach-API
Deutsche Schach-API für Python


| : Verfügbare Funktionen
| : Anleitung
| : Wichtige Hinweise
| : Variableninfo
| : Technische Details


Verfügbare Funktionen
-------------------
- visual_feldname
    Visualisiert die Feldnummer als Schachfeldname
- visual_farbe
    Visualisiert die Farbnummer als Farbnamen
- visual_farbenkürzel
    Visualisiert die Farbnummer als Farbkürzel
- visual_figur
    Visualisiert die Figurnummer als Figurennamen
- visual_figurkürzel
    Visualisiert die Figurnummer als Figurenkürzel
- tec_feldfarbe
    Gibt die technische Feldfarbe der angegebenen Feldnummer zurück
- neues_spiel
    Herstellen der Vaiablen für ein neues Spiel
- fstatus_func
    Herstellen der Statusvariable - Sortierung: Feld > Farbe >> Figur
- farbe_figur_auf_feld
    Ausgabe der Armeefarbe und Figur auf dem übermittelten Feld
- figurfelder_final
    Kompiliert die allgemein möglichen Figurfelder der Figur auf dem entsprechenden Startfeld mit den Minenfeldern, Fesselungen und Schachsituationen und gibt diese Liste aus.
- armeefiguren_final:
    Gibt final für die übergebene Farbe die Liste der bewegungsfähigen Figuren anhand deren Felder aus. Alle Funktionen wurden bercksichtigt darin.
- zug_final
    Führt den angegebenen Zug aus und aktualisiert kstatus, ep, roch und gibt zusätzlich die Umwandlung, Schachangriff, Schachmatt und Unentschieden(Patt) als bool aus.
- figur_umwandlung
    Konvertiert die Figur auf dem angegebenen Feld in die angegebene Figur (zulässig 1-6). Kann theoretisch für jede Umwandlung verwendet werden.

Anleitung
---------
1. **Spielstart:**
    Zum Spielstart müssen 3 Variablen lokal angelegt mit der Funktion :class:`neues_spiel` (:class:`kstatus, roch, ep = schach_api.neues_spiel()`).
2. **Spielfeldvisualisierung:**
    :class:`kstatus` ist ein Dictionary das von den Figuren ausgehend, deren besetzte Felder anzeigt, aufgebaut ist, man kann davon immer mit der Funktion :class:`fstatus_func` ein Dictionary herleiten, bei dem das Spielfeld die Referenz ist.
3. **Bei jedem Zug:**
    Mit der Funktion :class:`armeefiguren_final` erhältst du eine Liste der Figuren anhand ihrer Felder, die ziehen können und dürfen.
    Mit der Funktion :class:`armeefiguren_final` erhältst du eine Liste, welche Felder die ausgewähle Figur besetzen kann und darf.
    Mit der Funktion :class:`zug_final` setzt du den :class:`kstatus` neu anhand der angegebenen Figurbewegung
4. **Sonderfälle:**
    :class:`zug_final` gibt additional Informationen aus:
    4.1. **Umwandlung:**
        Mit der Funktion :class:`figur_umwandlung` setzt du den :class:`kstatus` neu anhand er angegebenen Figurkonvertierung.
    4.2. **Schach:**
        Wenn die gezogene Farbe den gegnerischen König angreift.
    4.3. **Schachmatt**
        Wenn die gezogene Farbe den gegnerischen König angreift und das Gegnerteam keinen Verteidigungszug ausführen kann.
    4.4. **Patt**
        Wenn die gezogene Farbe den gegnerischen König nicht angreift aber das Gegnerteam keinen Zug mehr ausführen kann.

WICHTIG
---------
- Die Funktion :class:`zug_final` prüft keine validen Züge, deswegen ist ein korrektes Spiel nur gewährleistet, wenn die richtigen Werte ordentlich weitergereicht werden. 💎

Variableninfo
-----------------
- ep
    EnPassant-Felder, die aktuell gültig sind
- roch
    Rochade-Felder, die aktuell gültig sind
- kstatus
    Allgemeine Statusvariable - beinhaltet so die Startsituation - Sortierung: Farbe > Figur >> Liste der Felder

Technische Details
---------
- **Spielfeld:**
    🔽 schwarz
    18  28	38	48	58	68	78	88
    17	27	37	47	57	67	77	87
    16	26	36	46	56	66	76	86
    15	25	35	45	55	65	75	85
    14	24	34	44	54	64	74	84
    13	23	33	43	53	63	73	83
    12	22	32	42	52	62	72	82
    11	21	31	41	51	61	71	81
    🔼 weiß
- **Farbe:**
    < *10* = w / Weiß ⚪
    < *-10* = s / Schwarz ⚫
    sollte *0* sein ist es als leer zu werten
- **Figuren:**
    < *1* = b / Bauer
    < *2* = s / Springer
    < *3* = l / Läufer
    < *4* = t / Turm
    < *5* = d / Dame
    < *6* = k / König
