import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser


def load_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    # Nettoyage des valeurs des sections
    for section in config.sections():
        for key in config[section]:
            # Supprimer les espaces en trop autour du nombre
            config[section][key] = config[section][key].strip()
            # Supprimer les commentaires après le nombre s'il y en a
            if ';' in config[section][key]:
                config[section][key] = config[section][key].split(';')[0].strip()

    return config

def wait_for_window(driver, window_data, timeout=2):
    time.sleep(timeout)  # le délai d'attente est déjà en secondes
    wh_now = driver.window_handles
    wh_then = window_data["window_handles"]
    if len(wh_now) > len(wh_then):
        return list(set(wh_now) - set(wh_then))[0]

def wait_until_clickable(driver, by, value, check_interval=60, max_timeout=6000):
    start_time = time.time()
    while time.time() - start_time < max_timeout:
        try:
            element = WebDriverWait(driver, check_interval).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except:
            print(
                "Le bouton n'est pas encore cliquable, vérification à nouveau dans {} secondes.".format(check_interval))
            time.sleep(check_interval)
    raise TimeoutError("Le bouton n'est pas devenu cliquable dans le délai imparti.")

def main():
    config = load_config('config.ini')

    window_data = {}  # Utilisation d'un dictionnaire pour stocker les données des fenêtres
    username = config['Credentials']['username']
    vote_retry_interval = int(config['CooldownTimes']['vote_retry_interval'])
    cooldown_duration = int(config['CooldownTimes']['cooldown_duration'])
    profile_path = config['Paths']['firefox_profile']

    # Configuration des options du navigateur
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")  # Utiliser Firefox en mode headless

    # Chemin vers l'exécutable Firefox
    firefox_path = "/snap/bin/firefox" 

    # Initialisation du service Firefox
    service = Service(executable_path=firefox_path)

    # Initialisation du pilote Firefox avec le service
    driver = webdriver.Firefox(service=service, options=firefox_options)
    try:
        # Étape 1 : Ouvrir l'URL cible
        driver.get("https://sydaria.fr/vote")

        # Étape 2 : Cliquer sur le champ de saisie
        driver.find_element(By.ID, "stepNameInput").click()

        # Étape 3 : Saisir le nom d'utilisateur
        driver.find_element(By.ID, "stepNameInput").send_keys(username)

        # Étape 4 : Appuyer sur Entrée
        driver.find_element(By.ID, "stepNameInput").send_keys(Keys.ENTER)

        # Étape 5 : Attendre que le bouton devienne cliquable et cliquer dessus
        window_data["window_handles"] = driver.window_handles
        vote_button = wait_until_clickable(driver, By.CSS_SELECTOR, ".btn:nth-child(1)", check_interval=vote_retry_interval,
                                           max_timeout=6000)

        # Boucle pour réessayer le clic toutes les minutes
        while True:
            try:
                # Clique sur le bouton
                vote_button.click()
                break  # Sort de la boucle si le clic réussit
            except:
                print("Le clic sur le bouton a échoué. Réessayer dans 1 minute.")
                time.sleep(vote_retry_interval)  # Attends une minute avant de réessayer

        # Étape 6 : Attendre que la nouvelle fenêtre s'ouvre
        window_data["win673"] = wait_for_window(driver, window_data, 2)

        # Étape 7 : Passer à la nouvelle fenêtre
        driver.switch_to.window(window_data["win673"])

        # Étape 8 : Cliquer sur le bouton de vote
        driver.find_element(By.ID, "voteBtn").click()

        # Étape 9 : Enregistrer le handle de la fenêtre actuelle (root)
        window_data["root"] = driver.current_window_handle

        # Étape 10 : Attendre que le nouvel onglet s'ouvre automatiquement
        window_data["window_handles_after_vote"] = driver.window_handles
        if len(window_data["window_handles_after_vote"]) > len(window_data["window_handles"]):
            window_data["server_priver_tab"] = \
            list(set(window_data["window_handles_after_vote"]) - set(window_data["window_handles"]))[0]
            driver.switch_to.window(window_data["server_priver_tab"])

        # Le nouvel onglet pour serveur-priver.fr doit maintenant être actif, vous pouvez ajouter d'autres actions si nécessaire

        # Attendre que le vote soit enregistré avec succès
        try:
            success_alert = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            print("Le vote a été enregistré avec succès.")
        except:
            print("Le vote n'a pas été enregistré avec succès. La fenêtre du serveur privé ne sera pas fermée.")

        # Fermer la fenêtre de serveur-prive.fr et revenir à la fenêtre d'origine
        driver.close()

        # Attendre le cooldown
        print(f"Attente du cooldown de {cooldown_duration} secondes...")
        time.sleep(cooldown_duration)

    finally:
        # Nettoyage : fermer le driver
        driver.quit()

if __name__ == "__main__":
    main()
