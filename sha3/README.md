# SHA3 (Keccak) Implementierung

## Übersicht

Dieses Paket enthält eine vollständige Implementierung der SHA3-Hash-Funktion (auch bekannt als Keccak) in Python. SHA3 ist ein kryptographischer Hash-Algorithmus, der von NIST im Jahr 2015 als Standard veröffentlicht wurde und eine Alternative zu den SHA-2-Hash-Funktionen darstellt.

## Funktionalitäten

### Unterstützte SHA3-Varianten

- **SHA3-224**: 224-Bit Hash-Ausgabe
- **SHA3-256**: 256-Bit Hash-Ausgabe  
- **SHA3-384**: 384-Bit Hash-Ausgabe
- **SHA3-512**: 512-Bit Hash-Ausgabe

### Kernfunktionen

Die Implementierung basiert auf der Keccak-f[1600]-Permutation mit folgenden Transformationsschritten:

1. **θ (Theta)**: Spaltenparität-Berechnung und XOR-Verknüpfung
2. **ρ (Rho)**: Bit-Rotation
3. **π (Pi)**: Lane-Permutation
4. **χ (Chi)**: Nichtlineare Transformation
5. **ι (Iota)**: Rundenkonstanten-Addition

## Dateien im Paket

### `sha3.py`
Die Hauptimplementierung der SHA3-Hash-Funktion mit folgenden Komponenten:

- **SHA3-Klasse**: Kernimplementierung mit allen Varianten
- **Hilfsfunktionen**: `sha3_224()`, `sha3_256()`, `sha3_384()`, `sha3_512()`
- **Datei-Hashing**: `hash_file()` für das Hashen von Dateien
- **Hex-Verarbeitung**: `process_hex_file()` für hexadezimale Eingabedateien

### `TestInput.txt`
Beispiel-Eingabedatei mit hexadezimalen Testdaten:
```
000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F
```

### `o.txt`
Ausgabedatei mit dem berechneten Hash-Wert (Beispiel für SHA3-224).

### `roundConstants.txt`
Datei mit den 24 Rundenkonstanten für die Keccak-f[1600]-Permutation.

## Verwendung

### Grundlegende Hash-Berechnung

```python
from sha3.sha3 import SHA3, sha3_256

# Verwendung der SHA3-Klasse
hasher = SHA3(256)  # SHA3-256 Variante
hasher.update(b"Hallo Welt")
hash_wert = hasher.hexdigest()
print(f"SHA3-256: {hash_wert}")

# Verwendung der Hilfsfunktionen
daten = b"Dies ist ein Test"
hash_wert = sha3_256(daten)
print(f"Hash: {hash_wert.hex()}")
```

### Verschiedene SHA3-Varianten

```python
from sha3.sha3 import SHA3

daten = b"Beispieltext für Hash-Berechnung"

# SHA3-224
hasher_224 = SHA3(224)
hasher_224.update(daten)
print(f"SHA3-224: {hasher_224.hexdigest()}")

# SHA3-256
hasher_256 = SHA3(256)
hasher_256.update(daten)
print(f"SHA3-256: {hasher_256.hexdigest()}")

# SHA3-384
hasher_384 = SHA3(384)
hasher_384.update(daten)
print(f"SHA3-384: {hasher_384.hexdigest()}")

# SHA3-512
hasher_512 = SHA3(512)
hasher_512.update(daten)
print(f"SHA3-512: {hasher_512.hexdigest()}")
```

### Datei-Hashing

```python
from sha3.sha3 import hash_file

# Hash einer Datei berechnen
dateipfad = "meine_datei.txt"
try:
    hash_wert = hash_file(dateipfad, 256)  # SHA3-256
    print(f"SHA3-256 der Datei: {hash_wert}")
except FileNotFoundError:
    print("Datei nicht gefunden")
```

### Schrittweise Hash-Berechnung

```python
from sha3.sha3 import SHA3

# Für große Datenmengen oder Stream-Verarbeitung
hasher = SHA3(256)

# Daten schrittweise hinzufügen
hasher.update(b"Erster Teil ")
hasher.update(b"der Nachricht")

# Finalen Hash abrufen
hash_wert = hasher.hexdigest()
print(f"Finaler Hash: {hash_wert}")
```

### Hexadezimale Eingabedateien verarbeiten

```python
from sha3.sha3 import process_hex_file

# Hexadezimale Daten aus Datei lesen und hashen
eingabe_datei = "hex_input.txt"  # Enthält: "48656C6C6F20576F726C64"
ausgabe_datei = "hash_output.txt"

try:
    process_hex_file(eingabe_datei, ausgabe_datei, 256)
    print("Hash erfolgreich berechnet und gespeichert")
except Exception as e:
    print(f"Fehler: {e}")
```

## Kommandozeilen-Nutzung

Das Modul kann direkt von der Kommandozeile ausgeführt werden:

```bash
# Grundlegende Nutzung (verwendet Standard-Dateien und SHA3-224)
python sha3.py

# Eigene Eingabe- und Ausgabedateien
python sha3.py input.txt output.txt

# Mit spezifischer Hash-Größe
python sha3.py input.txt output.txt 256

# SHA3-512 verwenden
python sha3.py TestInput.txt result.txt 512
```

### Parameter:
- **input_file**: Pfad zur Eingabedatei mit hexadezimalen Daten
- **output_file**: Pfad zur Ausgabedatei für den Hash-Wert
- **hash_size**: SHA3-Variante (224, 256, 384, 512) - Standard: 224

## Demo-Funktion

```python
from sha3.sha3 import demo

# Führt Demonstrationen mit verschiedenen Testfällen aus
demo()
```

Die Demo-Funktion zeigt:
- Hash-Berechnung für verschiedene Eingaben
- Alle SHA3-Varianten im Vergleich
- Datei-Hashing-Beispiel
- Performance-Tests

## Beispiele

### Beispiel 1: Einfacher Text-Hash

```python
from sha3.sha3 import sha3_256

nachricht = "Kryptographie ist spannend!"
hash_bytes = sha3_256(nachricht.encode('utf-8'))
print(f"SHA3-256: {hash_bytes.hex().upper()}")
```

### Beispiel 2: Große Datei hashen

```python
from sha3.sha3 import SHA3

def hash_grosse_datei(dateipfad):
    hasher = SHA3(256)
    
    with open(dateipfad, 'rb') as datei:
        while True:
            chunk = datei.read(8192)  # 8KB Blöcke
            if not chunk:
                break
            hasher.update(chunk)
    
    return hasher.hexdigest()

# Verwendung
hash_wert = hash_grosse_datei("grosse_datei.bin")
print(f"Hash der großen Datei: {hash_wert}")
```

### Beispiel 3: Hash-Vergleich für Datenintegrität

```python
from sha3.sha3 import sha3_256

# Original-Daten
original = b"Wichtige Daten"
original_hash = sha3_256(original).hex()

# Empfangene Daten (zum Vergleich)
empfangen = b"Wichtige Daten"
empfangen_hash = sha3_256(empfangen).hex()

if original_hash == empfangen_hash:
    print("Datenintegrität bestätigt!")
else:
    print("Warnung: Daten wurden verändert!")
```

## Technische Details

### Keccak-Sponge-Konstruktion

SHA3 verwendet die Sponge-Konstruktion mit folgenden Parametern:

| Variante | Rate (bits) | Capacity (bits) | Output (bits) |
|----------|-------------|-----------------|---------------|
| SHA3-224 | 1152        | 448             | 224           |
| SHA3-256 | 1088        | 512             | 256           |
| SHA3-384 | 832         | 768             | 384           |
| SHA3-512 | 576         | 1024            | 512           |
