# RSA-Verschlüsselungspaket

Dieses Paket implementiert das RSA-Kryptosystem, eine asymmetrische Verschlüsselungsmethode, die auf der Schwierigkeit der Faktorisierung großer zusammengesetzter Zahlen basiert.

## Überblick

Das RSA-Paket enthält zwei Hauptmodule:
- **Schlüsselgenerierung** (`rsa_keygen.py`): Generiert RSA-Schlüsselpaare
- **Ver-/Entschlüsselung** (`rsa.py`): Führt RSA-Operationen durch

## Dateibeschreibung

### Python-Module

#### `rsa_keygen.py`
Dieses Modul generiert RSA-Schlüsselpaare mit folgenden Funktionen:

- **Miller-Rabin-Primzahltest**: Probabilistischer Test zur Überprüfung der Primalität
- **Primzahlgenerierung**: Erzeugt große Primzahlen für die RSA-Schlüssel
- **Erweiterte Euklidische Algorithmus**: Berechnet modulare Inverse
- **Schlüsselpaar-Generierung**: Erstellt öffentliche und private RSA-Schlüssel

**Hauptfunktionen:**
- `generate_prime(bit_length)`: Generiert eine Primzahl mit gewünschter Bitlänge
- `generate_rsa_keypair(bit_length)`: Erzeugt ein vollständiges RSA-Schlüsselpaar
- `miller_rabin_test(n, k)`: Führt Primzahltest durch
- `mod_inverse(a, m)`: Berechnet modulare Inverse

#### `rsa.py`
Dieses Modul führt RSA-Ver- und Entschlüsselungsoperationen durch:

- **Square-and-Multiply-Algorithmus**: Effiziente modulare Exponentiation
- **Datei-Ein-/Ausgabe**: Liest Nachrichten und Schlüssel aus Dateien
- **RSA-Operation**: Führt die Grundoperation message^exponent mod modulus durch

**Hauptfunktionen:**
- `square_and_multiply(base, exponent, modulus)`: Effiziente modulare Exponentiation
- `rsa_operation(message, exponent, modulus)`: RSA-Hauptoperation
- `read_input_file(file_path)`: Liest Nachrichtendateien
- `read_key_file(file_path)`: Liest Schlüsseldateien

### Datendateien

#### Schlüsseldateien
- **`private.key`**, **`private_512.key`**: Private Schlüssel (d, n)
- **`public.key`**, **`public_512.key`**: Öffentliche Schlüssel (e, n)
- **`primes.txt`**, **`primes_512.txt`**: Primfaktoren (p, q)

#### Beispieldateien
- **`ExampleText.txt`**: Beispiel-Klartext (Nachricht: 20)
- **`ExampleKey.txt`**: Beispiel-Schlüssel für Verschlüsselung
- **`ExampleKeyDecrypt.txt`**: Beispiel-Schlüssel für Entschlüsselung
- **`ExampleEncrypted.txt`**: Beispiel-verschlüsselter Text
- **`test_message.txt`**: Test-Nachricht (12345)

## Verwendung

### 1. Schlüsselgenerierung

Um ein neues RSA-Schlüsselpaar zu generieren:

```powershell
python rsa_keygen.py <bit_länge> <private_schlüssel_datei> <öffentlicher_schlüssel_datei> <primfaktoren_datei>
```

**Parameter:**
- `bit_länge`: Gewünschte Bitlänge für den RSA-Modulus (z.B. 1024, 2048)
- `private_schlüssel_datei`: Ausgabedatei für den privaten Schlüssel
- `öffentlicher_schlüssel_datei`: Ausgabedatei für den öffentlichen Schlüssel
- `primfaktoren_datei`: Ausgabedatei für die Primfaktoren

**Beispiele:**

```powershell
# Generierung eines 1024-Bit RSA-Schlüsselpaars
python rsa_keygen.py 1024 private.key public.key primes.txt

# Generierung eines 2048-Bit RSA-Schlüsselpaars
python rsa_keygen.py 2048 private_2048.key public_2048.key primes_2048.txt

# Generierung eines 512-Bit RSA-Schlüsselpaars (nur für Tests!)
python rsa_keygen.py 512 private_512.key public_512.key primes_512.txt
```

**Ausgabe:**
```
RSA Key Generation
==================
Bit length: 1024
Private key file: private.key
Public key file: public.key
Primes file: primes.txt

Generating RSA key pair with 1024-bit modulus...
Generating first prime with ~512 bits...
First prime generated: 512 bits
Generating second prime with ~512 bits...
Second prime generated: 512 bits
Modulus n has 1024 bits
Public exponent e = 65537
Calculating private exponent...
Key pair generated and verified successfully!
Private key written to: private.key
Public key written to: public.key
Primes written to: primes.txt

Key generation completed successfully!
Modulus bit length: 1024
Public exponent: 65537
```

### 2. Verschlüsselung

Um eine Nachricht zu verschlüsseln:

```powershell
python rsa.py <nachricht_datei> <öffentlicher_schlüssel_datei> <verschlüsselt_datei>
```

**Beispiele:**

```powershell
# Verschlüsselung einer Testnachricht
python rsa.py test_message.txt public.key encrypted_message.txt

# Verschlüsselung des Beispieltexts
python rsa.py ExampleText.txt public.key my_encrypted.txt
```

**Ausgabe:**
```
Read message: 12345
Read exponent: 65537
Read modulus: 129504416642523392456153545860998630308308147667612194895253800255869434919153862401989888077834461759229047827272725921810937595901012800972512940689930938502686308268930273120049772398858485678228081105465299803622086101462704173737008810888150800218258528877357526774772340998419809421033595242121259062313
Performing RSA operation using Square and Multiply method...
Result: 89234750293847502938475029384750293847502938475029384750293847502938475029384750
Result written to: encrypted_message.txt
```

### 3. Entschlüsselung

Um eine verschlüsselte Nachricht zu entschlüsseln:

```powershell
python rsa.py <verschlüsselt_datei> <private_schlüssel_datei> <entschlüsselt_datei>
```

**Beispiele:**

```powershell
# Entschlüsselung einer verschlüsselten Nachricht
python rsa.py encrypted_message.txt private.key decrypted_message.txt

# Entschlüsselung des Beispiels
python rsa.py ExampleEncrypted.txt ExampleKeyDecrypt.txt decrypted_example.txt
```

**Ausgabe:**
```
Read message: 89234750293847502938475029384750293847502938475029384750293847502938475029384750
Read exponent: 82901234567890123456789012345678901234567890123456789012345678901234567890123456
Read modulus: 129504416642523392456153545860998630308308147667612194895253800255869434919153862401989888077834461759229047827272725921810937595901012800972512940689930938502686308268930273120049772398858485678228081105465299803622086101462704173737008810888150800218258528877357526774772340998419809421033595242121259062313
Performing RSA operation using Square and Multiply method...
Result: 12345
Result written to: decrypted_message.txt
```

## Dateiformat

### Nachrichtendateien
Enthalten eine einzige Dezimalzahl pro Datei:
```
12345
```

### Schlüsseldateien
Enthalten zwei Zeilen:
1. Exponent (e für öffentlich, d für privat)
2. Modulus (n)

**Beispiel öffentlicher Schlüssel:**
```
65537
129504416642523392456153545860998630308308147667612194895253800255869434919153862401989888077834461759229047827272725921810937595901012800972512940689930938502686308268930273120049772398858485678228081105465299803622086101462704173737008810888150800218258528877357526774772340998419809421033595242121259062313
```

### Primfaktoren-Dateien
Enthalten die beiden Primfaktoren p und q:
```
11398906462624143467801508247542039582891678987654321...
11367890123456789012345678901234567890123456789012345...
```

## Vollständiges Beispiel: Ver- und Entschlüsselung

Hier ist ein komplettes Beispiel für den gesamten Workflow:

```powershell
# 1. Schlüsselpaar generieren
python rsa_keygen.py 1024 mein_private.key mein_public.key meine_primes.txt

# 2. Nachricht erstellen
echo 42 > meine_nachricht.txt

# 3. Nachricht verschlüsseln
python rsa.py meine_nachricht.txt mein_public.key verschlüsselt.txt

# 4. Nachricht entschlüsseln
python rsa.py verschlüsselt.txt mein_private.key entschlüsselt.txt

# 5. Ergebnis überprüfen
type entschlüsselt.txt
# Ausgabe sollte: 42
```

## Wichtige Hinweise

### Sicherheit
- **Verwenden Sie mindestens 2048-Bit-Schlüssel** für produktive Umgebungen
- 512-Bit-Schlüssel sind nur für Demonstrationszwecke geeignet
- 1024-Bit-Schlüssel gelten heute als unsicher für kritische Anwendungen

### Leistung
- Die Schlüsselgenerierung kann bei größeren Bitlängen mehrere Minuten dauern
- Die Ver-/Entschlüsselung ist durch den Square-and-Multiply-Algorithmus optimiert
- Größere Schlüssel bedeuten längere Berechnungszeiten

### Limitierungen
- Nur numerische Nachrichten werden unterstützt
- Die Nachricht muss kleiner als der Modulus n sein
- Für Textverarbeitung ist eine zusätzliche Kodierung erforderlich

## Algorithmus-Details

### RSA-Algorithmus
1. **Schlüsselgenerierung:**
   - Wähle zwei große Primzahlen p und q
   - Berechne n = p × q
   - Berechne φ(n) = (p-1) × (q-1)
   - Wähle e mit gcd(e, φ(n)) = 1
   - Berechne d ≡ e⁻¹ (mod φ(n))

2. **Verschlüsselung:** c ≡ m^e (mod n)
3. **Entschlüsselung:** m ≡ c^d (mod n)

### Square-and-Multiply
Effiziente Methode zur Berechnung von a^b mod n:
- Binäre Darstellung des Exponenten
- Iterative Quadrierung und Multiplikation
- Zeitkomplexität: O(log b)

## Fehlerbehebung

### Häufige Fehler
1. **"Input file not found"**: Überprüfen Sie den Dateipfad
2. **"Invalid integer in input file"**: Datei muss eine gültige Dezimalzahl enthalten
3. **"Key file must contain exactly two lines"**: Schlüsseldatei hat falsches Format
4. **"Bit length must be at least 8"**: Verwenden Sie eine größere Bitlänge

### Debugging-Tipps
- Verwenden Sie kleine Beispiele zum Testen
- Überprüfen Sie Dateiformate sorgfältig
- Stellen Sie sicher, dass Nachrichten kleiner als der Modulus sind

## Weiterführende Informationen

- RSA wurde 1977 von Rivest, Shamir und Adleman entwickelt
- Basiert auf dem Problem der Ganzzahlfaktorisierung
- Weit verbreitet in modernen Kryptosystemen (HTTPS, SSH, etc.)
- Asymmetrische Verschlüsselung ermöglicht sichere Kommunikation ohne gemeinsame Geheimnisse
