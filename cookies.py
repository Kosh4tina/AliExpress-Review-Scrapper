import os
import time
import json
import pickle
from selenium import webdriver

# Loads configuration from a JSON file.
# Arguments:
# - config_file: Path to the configuration file (default: "assets/config.json").
# Returns:
# - A dictionary containing the configuration parameters.
def load_config(config_file="assets/config.json"):
    with open(config_file, "r") as file:
        config = json.load(file)
    print("Configuration loaded successfully.")
    return config


# Opens a browser for manual interaction to set the country and solve CAPTCHA.
# Once the user confirms, cookies are saved to a file for future use.
# Arguments:
# - url: The URL to navigate to for manual setup (e.g., AliExpress homepage).
# - cookie_file: Path to save the cookies file (default: "cookies.pkl").
def save_cookies(config):
    cookie_file = 'assets/cookies.pkl'
    if os.path.exists(cookie_file):
        print(f"Cookie file '{cookie_file}' already exists. Deleting it...")
        os.remove(cookie_file)
        print(f"Deleted '{cookie_file}' successfully.")

    print("Opening browser for manual interaction...")
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={config['browser']['user_data_dir']}")
    options.add_argument(f"--profile-directory={config['browser']['profile_directory']}")

    driver = webdriver.Chrome(options=options)
    url = "https://www.aliexpress.us";
    driver.get(url)
    input("Manually set the country and solve CAPTCHA. Press Enter to save cookies...")
    
    cookies = driver.get_cookies()
    with open(cookie_file, "wb") as file:
        pickle.dump(cookies, file)
    print(f"Cookies saved to {cookie_file}.")
    
    driver.quit()

# Main block to execute the function
if __name__ == "__main__":
    config = load_config()
    save_cookies(config)
