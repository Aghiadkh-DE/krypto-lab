# Diffie-Hellman Schlüsselaustausch

Das Diffie-Hellman-Paket implementiert das Diffie-Hellman-Schlüsselaustauschprotokoll, einen kryptographischen Algorithmus, der es zwei Parteien ermöglicht, über einen unsicheren Kanal einen gemeinsamen geheimen Schlüssel zu erstellen.

## Übersicht

Das Diffie-Hellman-Protokoll basiert auf der mathematischen Schwierigkeit des diskreten Logarithmusproblems. Es ermöglicht zwei Parteien (traditionell Alice und Bob), einen gemeinsamen geheimen Schlüssel zu generieren, ohne dass ein Angreifer, der die Kommunikation abhört, diesen Schlüssel bestimmen kann.

## Dateien im Paket

### 1. `modular_arithmetic.py`

**Zweck**: Stellt optimierte modulare Exponentiationsfunktionen zur Verfügung.

**Funktionalität**:
- Implementiert die Square-and-Multiply-Methode für effiziente modulare Exponentiation
- Behandelt Randfälle wie negative Exponenten und Modulus-Werte
- Essentiell für alle kryptographischen Berechnungen im Diffie-Hellman-Protokoll

**Hauptfunktion**:
```python
def mod_exp(base, exponent, modulus):
    """
    Berechnet (base^exponent) mod modulus effizient.
    
    Args:
        base (int): Die Basis
        exponent (int): Der Exponent (muss nicht-negativ sein)
        modulus (int): Der Modulus (muss positiv sein)
        
    Returns:
        int: Das Ergebnis von (base^exponent) mod modulus
    """
```

**Verwendungsbeispiel**:
```python
from diffie_hellman.modular_arithmetic import mod_exp

# Berechne 3^17 mod 19
result = mod_exp(3, 17, 19)
print(f"3^17 mod 19 = {result}")  # Ausgabe: 3^17 mod 19 = 7
```

### 2. `dh_params.py`

**Zweck**: Generiert sichere Parameter für das Diffie-Hellman-Protokoll.

**Funktionalität**:
- Generiert sichere Primzahlen (Safe Primes) der Form p = 2q + 1
- Findet geeignete Generatoren für die Gruppe Z*_p
- Verwendet Miller-Rabin-Primzahltests für hohe Sicherheit
- Stellt Kommandozeilen-Interface für Parametergenerierung bereit

**Hauptfunktionen**:
```python
def generate_safe_prime(bit_length, k=10):
    """
    Generiert eine sichere Primzahl p = 2q + 1.
    
    Args:
        bit_length (int): Gewünschte Bitlänge für p
        k (int): Anzahl der Miller-Rabin-Runden
        
    Returns:
        tuple: (p, q) wobei p = 2q + 1 und beide prim sind
    """

def find_generator(p, q):
    """
    Findet einen Generator g für die Gruppe Z*_p.
    
    Args:
        p (int): Die sichere Primzahl
        q (int): Die Sophie-Germain-Primzahl wobei p = 2q + 1
        
    Returns:
        int: Ein Generator g für Z*_p
    """
```

**Verwendungsbeispiel**:
```bash
# Parameter für 256-Bit-Primzahl generieren
python dh_params.py 256

# Ausgabe:
# Generating safe prime with approximately 256 bits...
# Safe prime p generated: 256 bits
# Sophie Germain prime q: 255 bits
# Finding generator...
# Generator g = 2
# DH parameters generated successfully!
# [Primzahl p]
# [Generator g]
```

**Programmatische Verwendung**:
```python
from diffie_hellman.dh_params import generate_safe_prime, find_generator

# Generiere eine 512-Bit sichere Primzahl
p, q = generate_safe_prime(512)
print(f"Sichere Primzahl p: {p}")
print(f"Sophie-Germain-Primzahl q: {q}")

# Finde einen Generator
g = find_generator(p, q)
print(f"Generator g: {g}")
```

### 3. `dh_exchange.py`

**Zweck**: Implementiert den eigentlichen Diffie-Hellman-Schlüsselaustausch.

**Funktionalität**:
- Generiert kryptographisch sichere private Schlüssel
- Berechnet öffentliche Werte basierend auf privaten Schlüsseln
- Führt den Schlüsselaustausch durch und berechnet den gemeinsamen geheimen Schlüssel
- Stellt Kommandozeilen-Interface für interaktiven Schlüsselaustausch bereit

**Hauptfunktionen**:
```python
def generate_private_key(p):
    """
    Generiert einen kryptographisch sicheren privaten Schlüssel.
    
    Args:
        p (int): Der Primmodulus
        
    Returns:
        int: Eine Zufallszahl a wobei 2 ≤ a < p-1
    """

def compute_public_value(g, a, p):
    """
    Berechnet den öffentlichen Wert A = g^a mod p.
    
    Args:
        g (int): Der Generator
        a (int): Der private Schlüssel
        p (int): Der Primmodulus
        
    Returns:
        int: Der öffentliche Wert A
    """

def compute_shared_secret(B, a, p):
    """
    Berechnet den gemeinsamen geheimen Schlüssel S = B^a mod p.
    
    Args:
        B (int): Der öffentliche Wert der anderen Partei
        a (int): Der eigene private Schlüssel
        p (int): Der Primmodulus
        
    Returns:
        int: Der gemeinsame geheime Schlüssel S
    """
```

**Verwendungsbeispiel (Kommandozeile)**:
```bash
# Erstelle zuerst Parameter
python dh_params.py 256 > params.txt

# Starte den Schlüsselaustausch
python dh_exchange.py < params.txt

# Das Programm erwartet:
# 1. Die Parameter p und g (aus params.txt)
# 2. Den öffentlichen Wert B der anderen Partei (Eingabe)
# 
# Ausgabe:
# [Eigener öffentlicher Wert A]
# [Gemeinsamer geheimer Schlüssel S]
```

**Programmatische Verwendung**:
```python
from diffie_hellman.dh_exchange import (
    generate_private_key, 
    compute_public_value, 
    compute_shared_secret
)

# Angenommene Parameter (normalerweise von dh_params.py generiert)
p = 23  # Primzahl
g = 5   # Generator

# Alice generiert ihren privaten Schlüssel und öffentlichen Wert
alice_private = generate_private_key(p)
alice_public = compute_public_value(g, alice_private, p)

# Bob generiert seinen privaten Schlüssel und öffentlichen Wert
bob_private = generate_private_key(p)
bob_public = compute_public_value(g, bob_private, p)

# Beide berechnen den gemeinsamen geheimen Schlüssel
alice_shared = compute_shared_secret(bob_public, alice_private, p)
bob_shared = compute_shared_secret(alice_public, bob_private, p)

print(f"Alice's gemeinsamer Schlüssel: {alice_shared}")
print(f"Bob's gemeinsamer Schlüssel: {bob_shared}")
print(f"Schlüssel stimmen überein: {alice_shared == bob_shared}")
```

## Vollständiges Beispiel: Diffie-Hellman-Schlüsselaustausch

Hier ist ein vollständiges Beispiel, das den gesamten Diffie-Hellman-Prozess demonstriert:

```python
from diffie_hellman.dh_params import generate_safe_prime, find_generator
from diffie_hellman.dh_exchange import (
    generate_private_key, 
    compute_public_value, 
    compute_shared_secret
)

def diffie_hellman_demo():
    """
    Demonstriert einen vollständigen Diffie-Hellman-Schlüsselaustausch.
    """
    print("=== Diffie-Hellman-Schlüsselaustausch Demo ===\n")
    
    # Schritt 1: Parameter generieren
    print("1. Parameter generieren...")
    bit_length = 64  # Kleine Bitlänge für Demo-Zwecke
    p, q = generate_safe_prime(bit_length)
    g = find_generator(p, q)
    
    print(f"   Primzahl p: {p}")
    print(f"   Generator g: {g}\n")
    
    # Schritt 2: Alice generiert ihre Schlüssel
    print("2. Alice generiert ihre Schlüssel...")
    alice_private = generate_private_key(p)
    alice_public = compute_public_value(g, alice_private, p)
    
    print(f"   Alice's privater Schlüssel: {alice_private}")
    print(f"   Alice's öffentlicher Wert: {alice_public}\n")
    
    # Schritt 3: Bob generiert seine Schlüssel
    print("3. Bob generiert seine Schlüssel...")
    bob_private = generate_private_key(p)
    bob_public = compute_public_value(g, bob_private, p)
    
    print(f"   Bob's privater Schlüssel: {bob_private}")
    print(f"   Bob's öffentlicher Wert: {bob_public}\n")
    
    # Schritt 4: Austausch der öffentlichen Werte (simuliert)
    print("4. Austausch der öffentlichen Werte...")
    print(f"   Alice sendet {alice_public} an Bob")
    print(f"   Bob sendet {bob_public} an Alice\n")
    
    # Schritt 5: Berechnung des gemeinsamen Geheimnisses
    print("5. Berechnung des gemeinsamen Geheimnisses...")
    alice_shared = compute_shared_secret(bob_public, alice_private, p)
    bob_shared = compute_shared_secret(alice_public, bob_private, p)
    
    print(f"   Alice berechnet: {bob_public}^{alice_private} mod {p} = {alice_shared}")
    print(f"   Bob berechnet: {alice_public}^{bob_private} mod {p} = {bob_shared}")
    
    # Schritt 6: Verifikation
    print(f"\n6. Verifikation:")
    print(f"   Gemeinsamer Schlüssel stimmt überein: {alice_shared == bob_shared}")
    print(f"   Gemeinsamer Schlüssel: {alice_shared}")

if __name__ == "__main__":
    diffie_hellman_demo()
```

## Sicherheitshinweise

1. **Sichere Parameter**: Verwenden Sie ausreichend große Primzahlen (mindestens 2048 Bit für produktive Umgebungen).

2. **Zufällige private Schlüssel**: Das Paket verwendet das `secrets`-Modul für kryptographisch sichere Zufallszahlen.

3. **Man-in-the-Middle-Angriffe**: Das Diffie-Hellman-Protokoll allein bietet keine Authentifizierung. In produktiven Umgebungen sollten zusätzliche Authentifizierungsmechanismen verwendet werden.

4. **Wiederverwendung von Schlüsseln**: Private Schlüssel sollten nicht wiederverwendet werden.

## Installation und Abhängigkeiten

Das Paket verwendet nur Python-Standardbibliotheken:
- `secrets` für kryptographisch sichere Zufallszahlen
- `random` für Parameter-Generierung
- `sys` und `os` für Systemfunktionen

Zusätzlich wird die `is_prime`-Funktion aus dem `rsa.rsa_keygen`-Modul verwendet.

## Verwendung in der Kommandozeile

### Parameter generieren:
```bash
python dh_params.py [bit_length] > parameters.txt
```

### Schlüsselaustausch durchführen:
```bash
python dh_exchange.py < input.txt
```

Das Eingabeformat für `dh_exchange.py`:
```
[Primzahl p]
[Generator g]
[Öffentlicher Wert der anderen Partei]
```

## Mathematische Grundlagen

Das Diffie-Hellman-Protokoll basiert auf folgenden mathematischen Konzepten:

1. **Diskrete Exponentation**: Berechnung von g^a mod p ist effizient möglich
2. **Diskreter Logarithmus**: Die Umkehrung (Finden von a gegeben g^a mod p) ist schwierig
3. **Sichere Primzahlen**: Primzahlen der Form p = 2q + 1 bieten zusätzliche Sicherheit
4. **Generatoren**: Elemente, die die gesamte Gruppe Z*_p erzeugen

## Lizenz

Dieses Paket ist Teil des krypto-lab Projekts und steht unter der entsprechenden Lizenz.