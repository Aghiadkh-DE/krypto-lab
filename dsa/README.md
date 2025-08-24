# Digital Signature Algorithm (DSA) Implementierung

Dieses Verzeichnis enthält eine vollständige Implementierung des Digital Signature Algorithm (DSA) gemäß den spezifizierten Anforderungen.

## Parameter
- **L = 1024**: Bitlänge der Primzahl p
- **N = 160**: Bitlänge der Primzahl q  
- **Hashfunktion**: SHA-224 (unter Verwendung von Pythons hashlib-Bibliothek)
- **Verschlüsselung**: ElGamal-ähnlicher Ansatz

## Öffentliche Parameter
- **q**: Primzahl der Länge N (160 Bit)
- **p**: Primzahl der Länge L (1024 Bit), wobei p = k·q + 1
- **g**: Gruppenelement mit Ordnung q
- **x**: Geheimer Schlüssel mit 1 < x < q
- **y**: Öffentlicher Schlüssel wobei y = g^x mod p

## Dateien

### 1. dsa_keygen.py
Erzeugt DSA-Parameter und Schlüsselpaare.

**Verwendung:**
```
python dsa_keygen.py [öffentliche_schlüssel_datei] [private_schlüssel_datei]
```

**Ausgabe:** Zwei Dateien mit folgendem Format:
```
Zeile 1: Primzahl p
Zeile 2: Primzahl q  
Zeile 3: Gruppenelement g
Zeile 4: Schlüssel (x für privat, y für öffentlich)
```

### 2. dsa_sign.py
Erstellt digitale Signaturen für Nachrichten.

**Verwendung:**
```
python dsa_sign.py [private_schlüssel_datei] [nachrichten_datei]
```

**Ausgabe:** Erstellt `[nachrichten_datei].sig` mit:
```
Zeile 1: r-Komponente
Zeile 2: s-Komponente
```

**Signatur-Algorithmus:**
1. Berechne H(m) mit SHA-224
2. Generiere zufällige Zahl k mit 1 < k < q
3. Berechne r = (g^k mod p) mod q
4. Berechne s = k^(-1)(H(m) + r·x) mod q
5. Falls r = 0 oder s = 0, wähle anderes k

### 3. dsa_verify.py
Verifiziert digitale Signaturen.

**Verwendung:**
```
python dsa_verify.py [öffentliche_schlüssel_datei] [nachrichten_datei]
```

**Eingabe:** Liest Signatur aus `[nachrichten_datei].sig`

**Verifikations-Algorithmus:**
1. Berechne w = s^(-1) mod q
2. Berechne u1 = H(m)·w mod q
3. Berechne u2 = r·w mod q  
4. Berechne v = (g^u1 · y^u2 mod p) mod q
5. Signatur ist gültig wenn v = r

## Beispiel-Verwendung

1. **Schlüssel generieren:**
```bash
python dsa_keygen.py public.key private.key
```

2. **Nachricht signieren:**
```bash
python dsa_sign.py private.key message.txt
```

3. **Signatur verifizieren:**
```bash
python dsa_verify.py public.key message.txt
```

## Implementierungsdetails

### Primzahlerzeugung
- Verwendet Miller-Rabin Primzahltest mit 20 Runden
- Generiert zuerst q (160 Bit)
- Findet p = k·q + 1 mit korrekter Bitlänge (1024 Bit)

### Gruppenelement-Erzeugung
- Sucht nach h wobei g = h^k mod p ≠ 1
- Verifiziert dass g Ordnung q hat durch Prüfung von g^q ≡ 1 (mod p)

### Sicherheitsmerkmale
- Zufällige k-Generierung für jede Signatur
- Ordnungsgemäße Bereichsprüfung für Signaturkomponenten
- SHA-224 Hashfunktion wie spezifiziert
- Modulare Inverse Berechnung mit erweitertem Euklidischen Algorithmus

## Mathematischer Hintergrund

Der DSA-Algorithmus bietet:
- **Authentifizierung**: Verifiziert Absender der Nachricht
- **Nichtabstreitbarkeit**: Absender kann Signierung nicht leugnen
- **Integrität**: Erkennt Nachrichtenverfälschung

Sicherheit beruht auf:
- Schwierigkeit des diskreten Logarithmusproblem
- Kryptographisch sichere Hashfunktion (SHA-224)
- Ordnungsgemäße Zufallszahlenerzeugung für k-Werte
