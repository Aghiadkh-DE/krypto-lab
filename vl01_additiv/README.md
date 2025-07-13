# Additive Cipher (Caesar-Verschlüsselung)

Implementierung einer additiven Verschlüsselung (Caesar-Cipher) mit automatischer Frequenzanalyse für deutsche Texte.

## Dateien

- `additive_cipher.py` - Ver- und Entschlüsselung mit Schlüssel
- `frequency_analysis_auto.py` - Automatische Entschlüsselung durch Frequenzanalyse
- `Klartext_1.txt` - Beispiel-Klartext
- `Kryptotext_1_Key_7.txt` - Verschlüsselter Text (Schlüssel 7)

## Verwendung

### Verschlüsselung/Entschlüsselung

**Verschlüsseln:**
```bash
python additive_cipher.py -i Klartext_1.txt -k 7 -o verschluesselt.txt -e
```

**Entschlüsseln:**
```bash
python additive_cipher.py -i Kryptotext_1_Key_7.txt -k 7 -o entschluesselt.txt -d
```

**Parameter:**
- `-i` - Eingabedatei
- `-k` - Schlüssel (0-25)
- `-o` - Ausgabedatei
- `-e` - Verschlüsseln
- `-d` - Entschlüsseln

### Automatische Frequenzanalyse

Entschlüsselt deutsche Texte automatisch ohne bekannten Schlüssel:

```bash
python frequency_analysis_auto.py Kryptotext_1_Key_7.txt entschluesselt.txt
```

Mit detaillierter Ausgabe:
```bash
python frequency_analysis_auto.py Kryptotext_1_Key_7.txt entschluesselt.txt -v
```

## Funktionsweise

Die Caesar-Verschlüsselung verschiebt jeden Buchstaben um eine feste Anzahl Positionen im Alphabet. Die Frequenzanalyse nutzt die Tatsache, dass 'E' der häufigste Buchstabe im Deutschen ist, um den Schlüssel automatisch zu ermitteln.

**Algorithmus:**
```
Verschlüsselung: (Buchstabe + Schlüssel) mod 26
Entschlüsselung: (Buchstabe - Schlüssel) mod 26
```

**Hinweis:** Nur Großbuchstaben A-Z werden verschlüsselt. Andere Zeichen bleiben unverändert.
