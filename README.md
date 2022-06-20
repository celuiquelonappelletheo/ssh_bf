# ssh_bf

Vous trouverez ci-dessous un script conçu pour effectuer du brute force sur le service ssh.

Attention: il s'agit d'une bêta qui ne gère pas toutes les erreurs. De plus, cette version est susceptible de contenir des erreurs.

# Installation

    git clone ...

    pip install paramiko

# Utilisation

Tout d'abord rendez-vous dans le dossier contenant le script ssh_bf.py

Pour executer le script utiliser la commande:

    python ./ssh_bf.py [vos options]

# Option disponible

    [-u] pour utiliser un nom d'utilisateur
    [-U] [chemin d'accès] pour utiliser une liste de noms d'utilisateur
    [-p] pour utiliser un mot de passe
    [-P] [chemin d'accès] pour utiliser une liste de mots de passe
    [-h] pour parametrer l'hostanme/ip cible
    [-H] [chemin d'accès] pour parametrer une liste d'hostname/ip cible
    [-J] pour ajouter une ou plusieurs machines de rebond (host:user:pass:port,host:user:pass:port)

    [--port] pour définir le port sur lequel serons effectuer les connexions ssh
    
# Remarque:
Les ajouts d'options uniques et par importation de fichier sont cumulables.
