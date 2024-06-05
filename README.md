Voici un guide détaillé pour mettre en place et exécuter votre programme de vote automatique sur un serveur, en veillant à ce que toutes les étapes nécessaires soient couvertes.

### Étape 1: Configurer le Serveur

#### 1.1. Mettre à jour et installer les dépendances
Connectez-vous à votre serveur et mettez à jour les paquets:

```sh
sudo apt update && sudo apt upgrade -y
```

#### 1.2. Installer une Interface Graphique (GUI) légère
Installez XFCE, une interface graphique légère, ainsi que Firefox et `geckodriver`:

```sh
sudo apt install xfce4 xfce4-goodies -y
sudo apt install firefox -y
sudo apt install firefox-geckodriver -y
```

#### 1.3. Installer `xrdp` pour l'accès à distance
Installez et configurez `xrdp` pour permettre l'accès à distance:

```sh
sudo apt install xrdp -y
sudo systemctl enable xrdp
sudo systemctl start xrdp
```

Ajoutez votre utilisateur au groupe `ssl-cert` pour que `xrdp` puisse utiliser la clé SSL:

```sh
sudo adduser $USER ssl-cert
```

Créez ou modifiez le fichier `.xsession` pour lancer XFCE avec `xrdp`:

```sh
echo "startxfce4" > ~/.xsession
```

Redémarrez `xrdp` pour appliquer les modifications:

```sh
sudo systemctl restart xrdp
```

#### 1.4. Accéder au serveur via Bureau à Distance
Utilisez un client de bureau à distance comme Remote Desktop Connection (Windows), Remmina (Linux), ou Microsoft Remote Desktop (macOS) pour vous connecter au serveur. Utilisez l'adresse IP du serveur et les informations d'identification de votre utilisateur.

### Étape 2: Configurer l'environnement Python

#### 2.1. Installer Python et les dépendances
Installez Python et `pip`:

```sh
sudo apt install python3 python3-pip -y
```

#### 2.2. Créer un environnement virtuel
Créez et activez un environnement virtuel pour isoler les dépendances de votre projet:

```sh
python3 -m venv myenv
source myenv/bin/activate
```

#### 2.3. Installer les paquets nécessaires
Installez les paquets Python nécessaires à l'aide de `pip`:

```sh
pip install selenium pyautogui
```

### Étape 3: Déployer le Script de Vote

#### 3.1. Transférer le script sur le serveur
Utilisez `scp` ou un outil similaire pour transférer votre script Python sur le serveur.

Par exemple, sur votre machine locale, exécutez:

```sh
scp path/to/your/script.py username@server_ip:/path/on/server/
scp -r /local/path/to/Automatisation-Selenium-Remplir-Formulaire username@server_ip:/remote/path/
```

### Étape 4: Exécuter le Script

#### 4.1. Ouvrir une session `tmux` ou `screen`
Utilisez `tmux` ou `screen` pour exécuter le script en arrière-plan et maintenir la session active même après la déconnexion du terminal.

##### Utilisation de `tmux`:
Installez `tmux` si ce n'est pas déjà fait:

```sh
sudo apt install tmux -y
```

Créez une nouvelle session `tmux`:

```sh
tmux new -s vote_bot_session
```

##### Utilisation de `screen`:
Installez `screen` si ce n'est pas déjà fait:

```sh
sudo apt install screen -y
```

Créez une nouvelle session `screen`:

```sh
screen -S vote_bot_session
```

#### 4.2. Activer l'environnement virtuel et exécuter le script
Dans la session `tmux` ou `screen`, activez l'environnement virtuel et lancez le script:

```sh
cd /path/on/server/
source myenv/bin/activate
python3 script.py
```

#### 4.3. Détacher la session `tmux` ou `screen`
Pour détacher de la session `tmux` sans arrêter le script, appuyez sur `Ctrl + B`, puis sur `D`.

Pour détacher de la session `screen` sans arrêter le script, appuyez sur `Ctrl + A`, puis sur `D`.

Vous pouvez toujours revenir à la session en utilisant:

##### `tmux`:
```sh
tmux attach -t vote_bot_session
```

##### `screen`:
```sh
screen -r vote_bot_session
```

Avec ces étapes, votre script sera configuré pour fonctionner de manière continue sur le serveur avec la capacité d'effectuer des clics aux coordonnées spécifiées en utilisant `pyautogui`.