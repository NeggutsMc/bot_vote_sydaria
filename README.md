# Automatisation de vote avec Selenium

Ce script Python utilise Selenium pour automatiser le processus de vote sur un site web spécifique. Il remplit un formulaire de vote en ligne en saisissant un nom, en cliquant sur des boutons et en cochant une case de vérification "Je ne suis pas un robot".

## Prérequis

- Python 3.x installé sur votre système.
- Les bibliothèques Python suivantes doivent être installées :
  - Selenium
  - PyAutoGUI

Vous pouvez les installer en exécutant la commande suivante :
```
pip install selenium pyautogui
```

## Configuration du projet

1. Téléchargez et installez le navigateur web que vous souhaitez automatiser. Dans cet exemple, nous utilisons Mozilla Firefox.
2. Téléchargez le pilote (driver) pour le navigateur que vous avez choisi et configurez le chemin dans la fonction `initialize_browser()` du script Python.
3. Assurez-vous d'avoir un profil utilisateur personnalisé dans le répertoire spécifié dans la fonction `initialize_browser()` pour le navigateur. Cela peut être utile pour charger des extensions ou d'autres configurations spécifiques.
4. Dans la fonction `check_verify_button()`, remplacez les coordonnées `x_coord` et `y_coord` par les coordonnées de la case à cocher "Je ne suis pas un robot" sur votre navigateur. Vous pouvez utiliser l'outil de développement de votre navigateur pour trouver ces coordonnées.

## Utilisation

1. Exécutez le script Python `main.py`.
2. Le script ouvrira un navigateur Firefox et naviguera vers la page de vote spécifiée.
3. Il saisira un nom dans le formulaire de vote, cliquera sur le bouton "Continuer", puis cochera la case "Je ne suis pas un robot" pour valider le vote.
4. Assurez-vous de ne pas interagir avec le navigateur pendant l'exécution du script, car cela peut perturber le processus d'automatisation.

## Notes

- Assurez-vous d'avoir une connexion Internet active pendant l'exécution du script, car il dépend de l'accès au site web de vote.
- Ce script est fourni à titre d'exemple et peut nécessiter des ajustements en fonction de la structure spécifique du site web que vous souhaitez automatiser.

---

N'oubliez pas d'ajuster les instructions et les détails selon les besoins spécifiques de votre projet. Si vous avez d'autres questions ou besoin de plus d'informations, n'hésitez pas à demander !
