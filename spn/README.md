# SPN (Substitution-Permutation Network) Dokumentation

Das SPN-Paket implementiert ein 4-Runden Substitution-Permutation Network (SPN) Chiffre mit linearer Kryptoanalyse-Funktionalität. Dieses Paket enthält sowohl die Grundfunktionen der Verschlüsselung/Entschlüsselung als auch verschiedene Analysewerkzeuge für lineare Angriffe.

## Überblick der Dateien

### Kernimplementierung

#### `spn_cipher.py`
**Beschreibung:** Hauptimplementierung des SPN-Chiffres mit Verschlüsselung und Entschlüsselung.

**Funktionalität:**
- Implementiert eine 4-Runden SPN mit 16-Bit Blöcken
- Verwendet eine feste S-Box und Bit-Permutation
- Unterstützt ECB-Modus für mehrere Blöcke
- Bietet partielle Entschlüsselung für Kryptoanalyse

**Verwendung:**
```bash
python spn_cipher.py [Eingabedatei] [Schlüssel] [Ausgabedatei]
```

**Parameter:**
- `Eingabedatei`: Datei mit Hexadezimal-Daten zum Verschlüsseln
- `Schlüssel`: 16-Bit Schlüssel (4 Hex-Zeichen)
- `Ausgabedatei`: Ausgabedatei für verschlüsselte Daten

**Beispiel:**
```bash
# Verschlüsselung einer Datei
python spn_cipher.py test_plaintext.txt A5B3 output_ciphertext.txt

# Inhalt von test_plaintext.txt: ABCD5678DEADBEEF1234
# Schlüssel: A5B3
# Ausgabe in output_ciphertext.txt: verschlüsselte Hexadezimal-Werte
```

**Programmfunktionen:**
- `encrypt(plaintext_hex, key_hex)`: Verschlüsselt Hexadezimal-String
- `decrypt(ciphertext_hex, key_hex)`: Entschlüsselt Hexadezimal-String
- `encrypt_block(plaintext, key)`: Verschlüsselt einzelnen 16-Bit Block
- `decrypt_block(ciphertext, key)`: Entschlüsselt einzelnen 16-Bit Block

### Lineare Kryptoanalyse

#### `linear_attack.py`
**Beschreibung:** Implementiert lineare Kryptoanalyse-Angriffe gegen das SPN-Chiffre.

**Funktionalität:**
- Führt lineare Angriffe auf partielle Schlüsselbits durch
- Analysiert Klartext-Kryptotext-Paare
- Berechnet empirische Verzerrungen (Bias) für Schlüsselkandidaten
- Unterstützt 4-Bit und 8-Bit partielle Schlüsselangriffe

**Verwendung:**
```bash
python linear_attack.py [Klartexte] [Kryptotexte]
```

**Parameter:**
- `Klartexte`: Datei mit Klartext-Hex-Blöcken
- `Kryptotexte`: Datei mit entsprechenden Kryptotext-Hex-Blöcken

**Beispiel:**
```bash
# Linearer Angriff mit Beispieldaten
python linear_attack.py attack_plaintexts.txt attack_ciphertexts.txt

# Ausgabe zeigt wahrscheinlichste Schlüsselkandidaten:
# 4-bit partial key candidates (sorted by |bias|):
# A: bias=+0.125000, prob=0.625000
# 3: bias=-0.093750, prob=0.406250
```

**Programmfunktionen:**
- `linear_attack(plaintexts, ciphertexts, target_bits)`: Führt linearen Angriff durch
- `compute_linear_approximation(plaintext, last_round_input)`: Berechnet lineare Approximation
- `partial_decrypt_for_attack(ciphertext, partial_key_candidate)`: Partielle Entschlüsselung

### Analysewerkzeuge für lineare Approximationen

#### `linear_approximation_quality.py`
**Beschreibung:** Evaluiert die Qualität einer gegebenen linearen Approximation.

**Funktionalität:**
- Validiert Approximationspfade auf Korrektheit
- Berechnet Gesamtqualität mittels Piling-up-Lemma
- Überprüft Konsistenz zwischen Runden

**Verwendung:**
```bash
python linear_approximation_quality.py [S-Box] [Approximation]
```

**Parameter:**
- `S-Box`: 16 Hexadezimal-Zeichen für S-Box-Definition
- `Approximation`: 32 Hexadezimal-Zeichen für Eingabe/Ausgabe-Masken

**Beispiel:**
```bash
# Qualitätsbewertung einer Approximation
python linear_approximation_quality.py E4D12F8B3A6C590F 17000000000000000000000000000000

# Ausgabe: Qualitätswert basierend auf Piling-up-Lemma
# 0.046875 (für gültige Approximation)
# -1 (für ungültige Approximation)
```

**Programmfunktionen:**
- `validate_approximation_trail(approximations)`: Validiert Pfad-Konsistenz
- `calculate_approximation_quality(sbox, approximations)`: Berechnet Gesamtqualität

## Datendateien

### Testdaten
- `test_plaintext.txt`: Beispiel-Klartext für Tests (`ABCD5678DEADBEEF1234`)

### Angriffsdaten
- `attack_plaintexts.txt`: Große Sammlung von Klartext-Blöcken für lineare Angriffe
- `attack_ciphertexts.txt`: Entsprechende Kryptotext-Blöcke

## Technische Details

### S-Box Definition
Die verwendete S-Box ist:
```
0→E, 1→4, 2→D, 3→1, 4→2, 5→F, 6→B, 7→8,
8→3, 9→A, A→6, B→C, C→5, D→9, E→0, F→7
```

### Permutation
Die Bit-Permutation ordnet Bit-Positionen wie folgt um:
```
[1,5,9,13, 2,6,10,14, 3,7,11,15, 4,8,12,16] (1-indiziert)
[0,4,8,12, 1,5,9,13, 2,6,10,14, 3,7,11,15] (0-indiziert)
```

### Rundenfunktion
Jede der 4 Runden besteht aus:
1. Schlüsseladdition (XOR)
2. S-Box-Substitution
3. Bit-Permutation (außer in der letzten Runde)

## Verwendungsbeispiele

### Vollständige Verschlüsselung
```bash
# 1. Klartext in Datei speichern
echo "ABCD5678DEADBEEF" > plaintext.txt

# 2. Verschlüsseln mit Schlüssel A5B3
python spn_cipher.py plaintext.txt A5B3 ciphertext.txt

# 3. Ergebnis anzeigen
cat ciphertext.txt
```

### Linearer Angriff
```bash
# Angriff mit vorhandenen Daten durchführen
python linear_attack.py attack_plaintexts.txt attack_ciphertexts.txt
```

### Approximationsqualität testen
```bash
# Standard S-Box und Beispiel-Approximation
python linear_approximation_quality.py E4D12F8B3A6C590F 17000000000000000000000000000000
```

## Hinweise

- Alle Hex-Eingaben sind ohne Präfix (kein "0x")
- Dateien sollten nur Hexadezimal-Zeichen enthalten
- Leerzeichen und Zeilenumbrüche in Hex-Dateien werden ignoriert
- Schlüssel müssen exakt 4 Hexadezimal-Zeichen sein (16 Bit)
- Für lineare Angriffe werden mindestens 100 Klartext-Kryptotext-Paare empfohlen

## Fehlerbehandlung

Die Programme geben spezifische Fehlermeldungen aus bei:
- Falscher Anzahl von Kommandozeilenargumenten
- Ungültigen Hexadezimal-Zeichen
- Falscher Schlüssellänge
- Nicht gefundenen Dateien
- Unpassenden Datenmengen zwischen Klartext und Kryptotext
