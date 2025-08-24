# Vigenère-Verschlüsselung

## Übersicht

Das Vigenère-Paket implementiert die klassische Vigenère-Verschlüsselung sowie automatische Kryptoanalyse-Werkzeuge zur Entschlüsselung von Vigenère-Chiffren ohne Kenntnis des Schlüssels.

## Dateien

### `vigenere_cipher.py`
Implementiert die grundlegende Vigenère-Verschlüsselung. Verschlüsselt Klartext mit einem gegebenen Schlüssel.

### `frequency_analysis_auto.py`
Automatisches Kryptoanalyse-Tool, das Vigenère-Chiffren durch Häufigkeitsanalyse und Index of Coincidence angreift. Bestimmt automatisch die Schlüssellänge und den Schlüssel.

## Verwendung

### Verschlüsselung

```bash
python vigenere_cipher.py -i Klartext_1.txt -k TAG -o verschluesselt.txt
```

**Parameter:**
- `-i`, `--input`: Eingabedatei mit dem Klartext
- `-k`, `--key`: Verschlüsselungsschlüssel (nur Großbuchstaben A-Z)
- `-o`, `--output`: Ausgabedatei für den Geheimtext

**Beispiel:**
```bash
python vigenere_cipher.py -i Klartext_1.txt -k INFORMATIK -o geheimtext.txt
```

### Automatische Kryptoanalyse

```bash
python frequency_analysis_auto.py -i Kryptotext_TAG.txt -o entschluesselt.txt
```

**Parameter:**
- `-i`, `--input`: Eingabedatei mit dem Geheimtext
- `-o`, `--output`: Ausgabedatei für den entschlüsselten Text

Das Tool gibt automatisch den gefundenen Schlüssel und die Schlüssellänge in der Konsole aus.

## Funktionsweise

### Vigenère-Verschlüsselung
Die Vigenère-Verschlüsselung verwendet einen sich wiederholenden Schlüssel zur Verschiebung der Buchstaben:
- Jeder Buchstabe des Klartexts wird um die Position des entsprechenden Schlüsselbuchstabens im Alphabet verschoben
- Nur alphabetische Zeichen (A-Z) werden verschlüsselt
- Andere Zeichen bleiben unverändert

### Automatische Kryptoanalyse
Das Analysewerkzeug verwendet mehrere Techniken:

1. **Index of Coincidence (IoC)**: Bestimmt die wahrscheinliche Schlüssellänge
2. **Chi-Quadrat-Test**: Findet den besten Verschiebungswert für jeden Schlüsselbuchstaben
3. **Deutsche Häufigkeitsanalyse**: Verwendet deutsche Buchstabenhäufigkeiten für optimale Ergebnisse

## Beispieldateien

- `Klartext_1.txt`: Beispiel-Klartext über Informatik
- `Kryptotext_TAG.txt`: Mit dem Schlüssel "TAG" verschlüsselter Text

## Algorithmus-Details

### Verschlüsselung
```
verschlüsselter_buchstabe = (klartext_buchstabe + schlüssel_buchstabe) mod 26
```

### Entschlüsselung
```
klartext_buchstabe = (verschlüsselter_buchstabe - schlüssel_buchstabe + 26) mod 26
```

### Index of Coincidence
Der IoC misst die Wahrscheinlichkeit, dass zwei zufällig ausgewählte Buchstaben identisch sind:
```
IoC = Σ(fi * (fi - 1)) / (n * (n - 1))
```
Wo `fi` die Häufigkeit des Buchstabens i und `n` die Textlänge ist.

## Einschränkungen

- Funktioniert optimal mit deutschen Texten
- Schlüssel müssen nur aus Großbuchstaben A-Z bestehen
- Die automatische Analyse benötigt ausreichend Text für zuverlässige Ergebnisse (mindestens 100-200 Zeichen)
