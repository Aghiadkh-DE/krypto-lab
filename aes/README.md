# AES (Advanced Encryption Standard) - Dokumentation

## Überblick

Diese Implementierung stellt eine vollständige AES-128 Verschlüsselung mit verschiedenen Betriebsmodi zur Verfügung.

## Dateien

- **`aes.py`** - Hauptimplementierung des AES-128 Algorithmus mit Schlüsselerweiterung, Ver- und Entschlüsselung
- **`operation_modes.py`** - Betriebsmodi: ECB, CBC, OFB, CTR
- **`SBox.txt`** / **`SBoxInvers.txt`** - AES S-Box Tabellen
- **`Beispiel_key.txt`** - Beispielschlüssel (11 Rundenschlüssel)
- **`simple_key.txt`** - Einfacher 128-Bit Testschlüssel
- **`test_iv.txt`** / **`test_nonce.txt`** - Initialisierungsvektor und Nonce für Tests
- **Beispieldateien** - Klartext- und Kryptotextbeispiele

## Verwendung

### Kommandozeile

```bash
python aes.py [MODE] [INPUT_FILE] [KEY_FILE] [OUTPUT_FILE] [IV_FILE]
```

**Parameter:**
- **MODE**: ECB, CBC, OFB, CTR
- **INPUT_FILE**: Hex-formatierte Eingabedatei
- **KEY_FILE**: 128-Bit Schlüssel in Hex
- **OUTPUT_FILE**: Ausgabedatei
- **IV_FILE**: IV/Nonce-Datei (für CBC, OFB, CTR)

### Beispiele

```bash
# ECB-Verschlüsselung
python aes.py ECB Beispiel_1_Klartext.txt simple_key.txt output.txt

# CBC-Verschlüsselung
python aes.py CBC Beispiel_1_Klartext.txt simple_key.txt output.txt test_iv.txt

# CTR-Verschlüsselung
python aes.py CTR Beispiel_1_Klartext.txt simple_key.txt output.txt test_nonce.txt
```

### Programmatische Verwendung

```python
from aes import aes_encrypt_wrapper, aes_decrypt_wrapper
from operation_modes import mode_cbc_encrypt, mode_cbc_decrypt

# Schlüssel und Daten
key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
plaintext = b"Hello World!!!!!"  # 16 Bytes
iv = bytes.fromhex("00112233445566778899aabbccddeeff")

# Verschlüsselung
ciphertext = mode_cbc_encrypt(16, aes_encrypt_wrapper, plaintext, key, iv)

# Entschlüsselung
decrypted = mode_cbc_decrypt(16, aes_decrypt_wrapper, ciphertext, key, iv)
```

## Betriebsmodi

- **ECB**: Einfachster Modus (nur für Tests)
- **CBC**: Empfohlen für allgemeine Verschlüsselung
- **OFB**: Stromchiffre-Modus
- **CTR**: Parallelisierbarer Stromchiffre-Modus

## Dateiformat

Alle Dateien verwenden Hexadezimalformat:
```
2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c
```

## Abhängigkeiten

- Python 3.x
- `util.file_util` (für Dateieingabe)
