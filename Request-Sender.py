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
