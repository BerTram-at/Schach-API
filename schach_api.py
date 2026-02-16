"""
# Schach-API

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
    Herstellen der Variablen für ein neues Spiel
- fstatus_func
    Herstellen der Statusvariable - Sortierung: Feld > Farbe >> Figur
- farbe_figur_auf_feld
    Ausgabe der Armeefarbe und Figur auf dem übermittelten Feld
- figurfelder_final
    Kompiliert die allgemein möglichen Figurfelder der Figur auf dem entsprechenden Startfeld mit den Minenfeldern, Fesselungen und Schachsituationen und gibt diese Liste aus.
- armeefiguren_final:
    Gibt final für die übergebene Farbe die Liste der bewegungsfähigen Figuren anhand deren Felder aus. Alle Funktionen wurden berücksichtigt darin.
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
    Mit der Funktion :class:`figurfelder_final` erhältst du eine Liste, welche Felder die ausgewähle Figur besetzen kann und darf.
    Mit der Funktion :class:`zug_final` setzt du den :class:`kstatus` neu anhand der angegebenen Figurbewegung
4. **Sonderfälle:**
    :class:`zug_final` gibt zusätzliche Informationen aus:
    4.1. **Umwandlung:**
        Mit der Funktion :class:`figur_umwandlung` setzt du den :class:`kstatus` neu anhand der angegebenen Figurkonvertierung.
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
"""
from copy import deepcopy

__version__ = "16-Feb-2026 10:00"

def _strer(x: str | int) -> str:
    return str(x)
def _quersumme(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))


_allefelder = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88]
_farben = {10: "weiß", -10: "schwarz"}
_farbenkürzel = {10: "w", -10: "s", 0: "c"}
_figuren = {1: "Bauer", 2: "Springer", 3: "Läufer", 4: "Turm", 5: "Dame", 6: "König"}
_figurenkürzel = {1: "b", 2: "s", 3: "l", 4: "t", 5: "d", 6: "k", 0: "c"}


_bauernweg = {10: [+1, 2, +11, -9, 8], -10: [-1, 7, -11, +9, 1]}
"""
I 0 : Ein Feld vorwärts
I 1 : Startfeld%10 muss gleich sein - indexiert die Startreihe
I 2 : Ein Feld diagonal vorwärts rechts
I 3 : Ein Feld diagonal vorwärts links
I 4 : Zielfeld%10 muss gleich sein - indexiert die gegn. Grundreihe
"""
_springerweg = [-8, +12, +21, +19, +8, -12, -21, -19]
_läuferweg = [+11, +9, -11, -9]
_turmweg = [+10, +1, -10, -1]
_damenweg = _läuferweg + _turmweg
_königweg = _damenweg

def visual_feldname(feld: int | str) -> str:
    """
    Zulässig: von 11 bis 88, Zahlen mit 9 oder 0 ausgenommen
    """
    o = _strer(feld)
    match o[0]:
        case "1":
            return "A" + o[1]
        case "2":
            return "B" + o[1]
        case "3":   
            return "C" + o[1]
        case "4":
            return "D" + o[1]   
        case "5":
            return "E" + o[1]
        case "6":
            return "F" + o[1]
        case "7":
            return "G" + o[1]
        case "8":
            return "H" + o[1]
def visual_farbe(x: int) -> str:
    """
    Zulässig: 10, -10
    """
    return _farben[x]
def visual_farbenkürzel(x: int) -> str:
    """
    Zulässig: 10, -10, 0
    """
    return _farbenkürzel[x]
def visual_figur(figur: int) -> str:
    """
    Zulässig: 1-6
    """
    return _figuren[figur]
def visual_figurkürzel(figur: int) -> str:
    """
    Zulässig: 1-6
    """
    return _figurenkürzel[figur]
def tec_feldfarbe(feld: int) -> int:
    """
    Zulässig: von 11 bis 88, Zahlen mit 9 oder 0 ausgenommen
    """
    if _quersumme(feld) % 2 == 0:
        return -10
    return 10


ep: list[int] = []
"""EnPassant-Felder, die aktuell gültig sind"""
roch: list[int] = [11, 18, 51, 58, 81, 88]
"""Rochade-Felder, die aktuell gültig sind"""
kstatus: dict[int, dict[int, list[int]]] = {10: {1: [12, 22, 32, 42, 52, 62, 72, 82], 2: [21, 71], 3: [31, 61], 4: [11, 81], 5: [41], 6: [51]}, -10: {1: [17, 27, 37, 47, 57, 67, 77, 87], 2: [28, 78], 3: [38, 68], 4: [18, 88], 5: [48], 6: [58]}}
"""Allgemeine Statusvariable - beinhaltet so die Startsituation - Sortierung: Farbe > Figur > Liste der Felder"""

def neues_spiel() -> tuple[dict[int, dict[int, list[int]]], list[int], list[int]]:
    """
    Herstellen der Variablen für ein neues Spiel
    
    Return
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    - roch:
        :class:`list[int]`
        Rochadeliste
    - ep:
        :class:`list[int]`
        ep-Liste
    """
    return deepcopy(kstatus), deepcopy(roch), deepcopy(ep)

def fstatus_func(kstatus: dict[int, dict[int, list[int]]]) -> dict[int, dict[int, int]]:
    """
    Herstellen der Statusvariable - Sortierung: Feld > Farbe >> Figur

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    
    Return
    -------
    - fstatus:
        :class:`dict[int, dict[int, int]]`
    """
    fstatus: dict[int, dict[int, int]] = {x: {0: 0} for x in _allefelder}
    for fa, farbe in kstatus.items():
        for fi, felder in farbe.items():
            for feld in felder:
                fstatus[feld] = {fa: fi}
    return fstatus

def farbe_figur_auf_feld(kstatus: dict[int, dict[int, list[int]]], feld: int) -> tuple[int, int]:
    """
    Ausgabe der Armeefarbe und Figur auf dem übermittelten Feld

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    - feld:
        :class:`int`
        Feldnummer
    
    Return
    -------
    - farbe:
        :class:`int`
    - figur:
        :class:`int`
    """
    fstatus = fstatus_func(kstatus)
    farbe, figur = next(iter(fstatus[feld].items()))
    return farbe, figur


def _figurfelder(kstatus: dict[int, dict[int, list[int]]], ep: list[int], roch: list[int], startfeld: int) -> list[int]:
    """
    Berechnet alle möglichen Zielfelder der Figur auf dem entsprechenden Startfeld unter Berücksichtigung von EnPassant, Rochade, Brettbegrenzung und Figurenblockaden

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    - ep:
        :class:`list[int]`
        ep-Liste
    - roch:
        :class:`list[int]`
        Rochadeliste
    - startfeld:
        :class:`int`
        Startfeldnummer
    
    Return
    -------
    - figurfelderliste:
        :class:`list[int]`
    """
    ausgabe: list[int] = []
    farbe, figur = farbe_figur_auf_feld(kstatus, startfeld)
    match figur:
        case 1:
            bweg = _bauernweg[farbe]
            weg = bweg[0]
            sr = bweg[2]
            sl = bweg[3]
            if startfeld+weg in _allefelder:
                fa = farbe_figur_auf_feld(kstatus, startfeld+weg)[0]
                if fa == 0:
                    ausgabe.append(startfeld+weg)
                if startfeld+2*weg in _allefelder:
                    fa = farbe_figur_auf_feld(kstatus, startfeld+2*weg)[0]
                    if (fa == 0) and (startfeld%10 == bweg[1]):
                        ausgabe.append(startfeld+2*weg)
            for i in [startfeld+sr, startfeld+sl]:
                if i in _allefelder:
                    fa = farbe_figur_auf_feld(kstatus, i)[0]
                    if (fa == -farbe) or (i in ep):
                        ausgabe.append(i)
        case 2:
            for weg in _springerweg:
                if startfeld+weg in _allefelder:
                    fa = farbe_figur_auf_feld(kstatus, startfeld+weg)[0]
                    if fa != farbe:
                        ausgabe.append(startfeld+weg)
        case 3:
            for weg in _läuferweg:
                for m in range(1, 9):
                    if startfeld+m*weg not in _allefelder:
                        break
                    fa = farbe_figur_auf_feld(kstatus, startfeld+m*weg)[0]
                    if fa != farbe:
                        ausgabe.append(startfeld+m*weg)
                    else:
                        break
                    if fa != 0:
                        break
        case 4:
            for weg in _turmweg:
                for m in range(1, 9):
                    if startfeld+m*weg not in _allefelder:
                        break
                    fa = farbe_figur_auf_feld(kstatus, startfeld+m*weg)[0]
                    if fa != farbe:
                        ausgabe.append(startfeld+m*weg)
                    else:
                        break
                    if fa != 0:
                        break
        case 5:
            for weg in _damenweg:
                for m in range(1, 9):
                    if startfeld+m*weg not in _allefelder:
                        break
                    fa = farbe_figur_auf_feld(kstatus, startfeld+m*weg)[0]
                    if fa != farbe:
                        ausgabe.append(startfeld+m*weg)
                    else:
                        break
                    if fa != 0:
                        break
        case 6:
            for weg in _königweg:
                if startfeld+weg in _allefelder:
                    fa = farbe_figur_auf_feld(kstatus, startfeld+weg)[0]
                    if fa != farbe:
                        ausgabe.append(startfeld+weg)
            if (startfeld in roch) and (startfeld-40 in roch) and ([farbe_figur_auf_feld(kstatus, startfeld-10)[0], farbe_figur_auf_feld(kstatus, startfeld-20)[0], farbe_figur_auf_feld(kstatus, startfeld-30)[0]] == [0, 0, 0]):
                ausgabe.append(startfeld-20)
            if (startfeld in roch) and (startfeld+30 in roch) and ([farbe_figur_auf_feld(kstatus, startfeld+10)[0], farbe_figur_auf_feld(kstatus, startfeld+20)[0]] == [0, 0]):
                ausgabe.append(startfeld+20)
    return sorted(ausgabe)


def _zwischen_info_listen(kstatus: dict[int, dict[int, list[int]]], farbe: int) -> tuple[list[int], dict[int, list[int]], list[list[int]]]:
    """
    Berechnet **von** der angegebenen Farbe ausgehend
    - minenfelder, list[int]
    - fesselliste, dict[int, list[int]]
    - schachliste, list[list[int]]

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett
    - farbe:
        :class:`int`
        <  10 : weiß
        < -10 : schwarz
    
    Return
    -------
    - minenfelder:
        :class:`list[int]`
    - fesselliste:
        :class:`dict[int, list[int]]`
    - schachliste:
        :class:`list[list[int]]`
    """
    minenfelder: list[int] = []
    fesselliste: dict[int, list[int]] = {}
    schachliste: list[list[int]] = []
    fstatus = fstatus_func(kstatus)
    for b in kstatus[farbe][1]:
        for weg in [b+_bauernweg[farbe][2], b+_bauernweg[farbe][3]]:
            if weg in _allefelder:
                if weg not in minenfelder:
                    minenfelder.append(weg)
                if fstatus[weg] == {-farbe: 6}:
                    schachliste.append([b])
    for p in kstatus[farbe][2]:
        for weg in _springerweg:
            if p+weg in _allefelder:
                if p+weg not in minenfelder:
                    minenfelder.append(p+weg)
                if fstatus[p+weg] == {-farbe: 6}:
                    schachliste.append([p])
    for l in kstatus[farbe][3]:
        for weg in _läuferweg:
            fsf = 0
            fsl: list[int] = []
            mine = True
            schach = False
            for m in range(1, 9):
                feld = l+m*weg
                if feld not in _allefelder:
                    break
                else:
                    if mine:
                        if feld not in minenfelder:
                            minenfelder.append(feld)
                        fa, fi = farbe_figur_auf_feld(kstatus, feld)
                        if fa == -farbe:
                            if fi in [1, 2, 3, 4, 5]:
                                mine = False
                    if farbe in fstatus[feld]:
                        break
                    elif 0 in fstatus[feld]:
                        fsl.append(feld)
                        continue
                    elif -farbe in fstatus[feld]:
                        if fstatus[feld][-farbe] == 6:
                            if fsf == 0:
                                schachliste.append(sorted(fsl + [l]))
                                schach = True
                            else:
                                if fsf in fesselliste:
                                    exfsl = fesselliste[fsf].copy()
                                    neufsl: list[int] = list(set.intersection(*(set(l) for l in [exfsl, fsl])))
                                    fesselliste[fsf] = neufsl
                                else:
                                    fesselliste[fsf] = fsl
                                break
                        else:
                            if schach:
                                break
                            if fsf == 0:
                                fsf = feld
                                mine = False
                            else:
                                break
            
    for t in kstatus[farbe][4]:
        for weg in _turmweg:
            fsf = 0
            fsl: list[int] = []
            mine = True
            schach = False
            for m in range(1, 9):
                feld = t+m*weg
                if feld not in _allefelder:
                    break
                else:
                    if mine:
                        if feld not in minenfelder:
                            minenfelder.append(feld)
                        fa, fi = farbe_figur_auf_feld(kstatus, feld)
                        if fa == -farbe:
                            if fi in [1, 2, 3, 4, 5]:
                                mine = False
                    if farbe in fstatus[feld]:
                        break
                    elif 0 in fstatus[feld]:
                        fsl.append(feld)
                        continue
                    elif -farbe in fstatus[feld]:
                        if fstatus[feld][-farbe] == 6:
                            if fsf == 0:
                                schachliste.append(sorted(fsl + [t]))
                                schach = True
                            else:
                                if fsf in fesselliste:
                                    exfsl = fesselliste[fsf].copy()
                                    neufsl: list[int] = list(set.intersection(*(set(l) for l in [exfsl, fsl])))
                                    fesselliste[fsf] = neufsl
                                else:
                                    fesselliste[fsf] = fsl
                                break
                        else:
                            if schach:
                                break
                            if fsf == 0:
                                fsf = feld
                                mine = False
                            else:
                                break
    for d in kstatus[farbe][5]:
        for weg in _damenweg:
            fsf = 0
            fsl: list[int] = []
            mine = True
            schach = False
            for m in range(1, 9):
                feld = d+m*weg
                if feld not in _allefelder:
                    break
                else:
                    if mine:
                        if feld not in minenfelder:
                            minenfelder.append(feld)
                        fa, fi = farbe_figur_auf_feld(kstatus, feld)
                        if fa == -farbe:
                            if fi in [1, 2, 3, 4, 5]:
                                mine = False
                    if farbe in fstatus[feld]:
                        break
                    elif 0 in fstatus[feld]:
                        fsl.append(feld)
                        fsl.sort()
                        continue
                    elif -farbe in fstatus[feld]:
                        if fstatus[feld][-farbe] == 6:
                            if fsf == 0:
                                schachliste.append(sorted(fsl + [d]))
                                schach = True
                            else:
                                if fsf in fesselliste:
                                    exfsl = fesselliste[fsf].copy()
                                    neufsl: list[int] = list(set.intersection(*(set(l) for l in [exfsl, fsl])))
                                    fesselliste[fsf] = neufsl
                                else:
                                    fesselliste[fsf] = fsl
                                break
                        else:
                            if schach:
                                break
                            if fsf == 0:
                                fsf = feld
                                mine = False
                            else:
                                break
    for k in kstatus[farbe][6]:
        for weg in _königweg:
            if k+weg in _allefelder:
                if k+weg not in minenfelder:
                    minenfelder.append(k+weg)
    return sorted(minenfelder), fesselliste, sorted(schachliste)


def figurfelder_final(kstatus: dict[int, dict[int, list[int]]], ep: list[int], roch: list[int], startfeld: int) -> list[int]:
    """
    Kompiliert die allgemein möglichen Figurfelder der Figur auf dem entsprechenden Startfeld mit den Minenfeldern, Fesselungen und Schachsituationen und gibt diese Liste aus.

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett  
    - ep:
        :class:`list[int]`
        ep-Liste
    - roch:
        :class:`list[int]`
        Rochadeliste
    - startfeld:
        :class:`int`
        Startfeldnummer
    
    Return
    -------
    - figurfelderliste:
        :class:`list[int]`
    """
    figurfelderliste = _figurfelder(kstatus, ep, roch, startfeld)
    farbe, figur = farbe_figur_auf_feld(kstatus, startfeld)
    minenfelder, fesselliste, schachliste = _zwischen_info_listen(kstatus, -farbe)
    if figur == 6:
        ff = figurfelderliste.copy()
        for feld in ff:
            if feld in minenfelder:
                if feld not in figurfelderliste:
                    continue
                figurfelderliste.remove(feld)
                if feld-startfeld == 10:
                    if feld+20 in figurfelderliste:
                        figurfelderliste.remove(feld+20)
                elif feld-startfeld == -10:
                    if feld-20 in figurfelderliste:
                        figurfelderliste.remove(feld-20)
    else:
        if startfeld in fesselliste:
            ff = figurfelderliste.copy()
            for feld in ff:
                if feld not in fesselliste[startfeld]:
                    if feld in figurfelderliste:
                        figurfelderliste.remove(feld)
        if len(schachliste) > 0:
            ss = list(set.intersection(*(set(l) for l in schachliste)))
            if len(ss) > 0:
                ff = figurfelderliste.copy()
                for feld in ff:
                    if feld in ep:
                        if feld-_bauernweg[farbe][0] not in ss:
                            if feld in figurfelderliste:
                                figurfelderliste.remove(feld)
                        else:
                            simks = deepcopy(kstatus)
                            simks[farbe][figur].remove(startfeld)
                            simks[farbe][figur].append(feld)
                            simks[-farbe][figur].remove(feld-_bauernweg[farbe][0])
                            _, _, sch = _zwischen_info_listen(simks, -farbe)
                            if len(sch) != 0:
                                if feld in figurfelderliste:
                                    figurfelderliste.remove(feld)
                    if feld not in ss:
                        if feld in figurfelderliste:
                            figurfelderliste.remove(feld)
            else:
                figurfelderliste.clear()
    return sorted(figurfelderliste)


def armeefiguren_final(kstatus: dict[int, dict[int, list[int]]], ep: list[int], roch: list[int], farbe: int) -> list[int]:
    """
    Gibt final für die übergebene Farbe die Liste der bewegungsfähigen Figuren anhand deren Felder aus. Alle Funktionen wurden berücksichtigt darin.

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett  
    - ep:
        :class:`list[int]`
        ep-Liste
    - roch:
        :class:`list[int]`
        Rochadeliste
    - farbe:
        :class:`int`
        Armeefarbe
    
    Return
    -------
    - armeeliste:
        :class:`list[int]`
    """
    ausgabe: list[int] = []
    armeeliste = kstatus[farbe]
    for fig in armeeliste.values():
        for feld in fig:
            x = figurfelder_final(kstatus, ep, roch, feld)
            if len(x) != 0:
                ausgabe.append(feld)
    return sorted(ausgabe)



def _zug(kstatus: dict[int, dict[int, list[int]]], ep: list[int], startfeld: int, zielfeld: int) -> tuple[dict[int, dict[int, list[int]]], list[int]]:
    """
    I : kstatus und ep werden aktualisiert und ausgegeben
    I : Schläge werden berücksichtigt
    I : roch wird nicht aktualisiert

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett  
    - ep:
        :class:`list[int]`
        ep-Liste
    - startfeld:
        :class:`int`
        Startfeldnummer
    - zielfeld:
        :class:`int`
        Zielfeldnummer
    
    Return
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
    - ep:
        :class:`list[int]`
    """
    fstatus = fstatus_func(kstatus)
    farbe, figur = farbe_figur_auf_feld(kstatus, startfeld)
    if fstatus[zielfeld] != {0: 0}:
        gegnerfarbe, gegnerfigur = farbe_figur_auf_feld(kstatus, zielfeld)
        kstatus[gegnerfarbe][gegnerfigur].remove(zielfeld)
    kstatus[farbe][figur].remove(startfeld)
    kstatus[farbe][figur].append(zielfeld)
    ep.clear()
    return kstatus, ep


def zug_final(kstatus: dict[int, dict[int, list[int]]], ep: list[int], roch: list[int], startfeld: int, zielfeld: int) -> tuple[dict[int, dict[int, list[int]]], list[int], list[int], bool, bool, bool, bool]:
    """
    Führt den angegebenen Zug aus und aktualisiert kstatus, ep, roch und gibt zusätzlich die Umwandlung, Schachangriff, Schachmatt und Unentschieden(Patt) als bool aus.

    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett  
    - ep:
        :class:`list[int]`
        ep-Liste
    - roch:
        :class:`list[int]`
        Rochadeliste
    - startfeld:
        :class:`int`
        Startfeldnummer
    - zielfeld:
        :class:`int`
        Zielfeldnummer

    Return
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
    - ep:
        :class:`list[int]`
    - roch:
        :class:`list[int]`
    - umwandlung:
        :class:`bool`  
    - schach:
        :class:`bool`
    - schachmatt:
        :class:`bool`
    - patt:
        :class:`bool`
    """
    umwandlung = False
    schach = False
    patt = False
    schachmatt = False
    oi = ep.copy()
    farbe, figur = farbe_figur_auf_feld(kstatus, startfeld)
    kstatusneu, epneu = _zug(kstatus, ep, startfeld, zielfeld)
    match figur:
        case 1:
            bauweg = _bauernweg[farbe][0]
            if zielfeld in oi:
                kstatusneu[-farbe][1].remove(zielfeld-bauweg)
            elif zielfeld-startfeld == 2*bauweg:
                epneu.append(startfeld+bauweg)
            elif zielfeld%10 == _bauernweg[farbe][4]:
                umwandlung = True
        case 4:
            if startfeld in roch:
                roch.remove(startfeld)
        case 6:
            if startfeld in roch:
                roch.remove(startfeld)
            if zielfeld-startfeld == 20:
                kk, epneu = _zug(kstatusneu, epneu, startfeld+30, zielfeld-10)
                kstatusneu = kk
                if startfeld+30 in roch:
                    roch.remove(startfeld+30)
            elif zielfeld-startfeld == -20:
                kk, epneu = _zug(kstatusneu, epneu, startfeld-40, zielfeld+10)
                kstatusneu = kk
                if startfeld-40 in roch:
                    roch.remove(startfeld-40)
    minenfelder, fesselliste, schachliste = _zwischen_info_listen(kstatusneu, farbe)
    x = armeefiguren_final(kstatusneu, epneu, roch, -farbe)
    if len(x) == 0:
        if len(schachliste) != 0:
            schachmatt = True
        else:
            patt = True
    if len(schachliste) != 0:
        schach = True
    return kstatusneu, epneu, sorted(roch), umwandlung, schach, schachmatt, patt



def figur_umwandlung(kstatus: dict[int, dict[int, list[int]]], ep: list[int], roch: list[int], feld: int, umwandlung_zu: int) -> tuple[dict[int, dict[int, list[int]]], bool, bool, bool]:
    """
    Konvertiert die Figur auf dem angegebenen Feld in die angegebene Figur (zulässig 1-6). Kann theoretisch für jede Umwandlung verwendet werden.
    
    Input
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
        Status der Figuren auf dem Schachbrett  
    - ep:
        :class:`list[int]`
        ep-Liste
    - feld:
        :class:`int`
        Feldnummer
    - umwandlung_zu:
        :class:`int`:
        < 1 : Bauer
        < 2 : Springer
        < 3 : Läufer
        < 4 : Turm
        < 5 : Dame
        < 6 : König

    Return
    -------
    - kstatus:
        :class:`dict[int, dict[int, list[int]]]`
    - schach:
        :class:`bool`
    - schachmatt:
        :class:`bool`
    - patt:
        :class:`bool`
    """
    schach = False
    patt = False
    schachmatt = False
    farbe, figur = farbe_figur_auf_feld(kstatus, feld)
    kstatus[farbe][figur].remove(feld)
    kstatus[farbe][umwandlung_zu].append(feld)
    minenfelder, fesselliste, schachliste = _zwischen_info_listen(kstatus, farbe)
    x = armeefiguren_final(kstatus, ep, roch, -farbe)
    if len(x) == 0:
        if len(schachliste) != 0:
            schachmatt = True
        else:
            patt = True
    if len(schachliste) != 0:
        schach = True
    return kstatus, schach, schachmatt, patt




