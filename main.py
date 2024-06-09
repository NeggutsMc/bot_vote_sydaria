import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
import os

def load_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    for section in config.sections():
        for key in config[section]:
            config[section][key] = config[section][key].strip()
            if ';' in config[section][key]:
                config[section][key] = config[section][key].split(';')[0].strip()

    return config

def wait_for_window(driver, window_data, timeout=2):
    time.sleep(timeout)
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

    window_data = {}
    username = config['Credentials']['username']
    vote_retry_interval = int(config['CooldownTimes']['vote_retry_interval'])
    cooldown_duration = int(config['CooldownTimes']['cooldown_duration'])
    profile_path = config['Paths']['firefox_profile']

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")

    # Utiliser xvfb-run pour exécuter Firefox avec Xvfb
    firefox_path = "/snap/bin/firefox"
    os.environ["PATH"] += os.pathsep + os.path.dirname(firefox_path)
    firefox_binary = f"xvfb-run --auto-servernum --server-args='-screen 0 1024x768x24' {firefox_path}"
    firefox_options.binary_location = firefox_binary

    service = Service(executable_path=firefox_path)

    driver = webdriver.Firefox(service=service, options=firefox_options)
    try:
        driver.get("https://sydaria.fr/vote")
        driver.find_element(By.ID, "stepNameInput").click()
        driver.find_element(By.ID, "stepNameInput").send_keys(username)
        driver.find_element(By.ID, "stepNameInput").send_keys(Keys.ENTER)

        window_data["window_handles"] = driver.window_handles
        vote_button = wait_until_clickable(driver, By.CSS_SELECTOR, ".btn:nth-child(1)", check_interval=vote_retry_interval,
                                           max_timeout=6000)

        while True:
            try:
                vote_button.click()
                break
            except:
                print("Le clic sur le bouton a échoué. Réessayer dans 1 minute.")
                time.sleep(vote_retry_interval)

        window_data["win673"] = wait_for_window(driver, window_data, 2)

        driver.switch_to.window(window_data["win673"])
        driver.find_element(By.ID, "voteBtn").click()

        window_data["root"] = driver.current_window_handle
        window_data["window_handles_after_vote"] = driver.window_handles
        if len(window_data["window_handles_after_vote"]) > len(window_data["window_handles"]):
            window_data["server_priver_tab"] = \
            list(set(window_data["window_handles_after_vote"]) - set(window_data["window_handles"]))[0]
            driver.switch_to.window(window_data["server_priver_tab"])

        try:
            success_alert = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            print("Le vote a été enregistré avec succès.")
        except:
            print("Le vote n'a pas été enregistré avec succès. La fenêtre du serveur privé ne sera pas fermée.")

        driver.close()

        print(f"Attente du cooldown de {cooldown_duration} secondes...")
        time.sleep(cooldown_duration)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
