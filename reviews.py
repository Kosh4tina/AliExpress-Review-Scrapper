import os
import time
import json
import random
import pickle
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initializes the Chrome WebDriver with specified options and profile.
# This function sets up the Selenium Chrome driver, including a custom user profile
# and other configurations, and returns the initialized WebDriver instance.
def init_driver(config):
    print("Initializing the WebDriver...")
    options = webdriver.ChromeOptions()

    # Use a specific user data directory and profile
    options.add_argument(f"user-data-dir={config['browser']['user_data_dir']}")
    options.add_argument(f"--profile-directory={config['browser']['profile_directory']}")

    # Additional common arguments to improve stability
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-features=MediaCodec,OutOfBlinkCors")
    options.add_argument("--log-level=3")  # Игнорировать незначительные ошибки
    # options.add_argument("--headless")  # Опционально, если без GUI

    # Specify the path to the ChromeDriver executable
    service = Service("assets/chromedriver.exe")

    # Initialize the WebDriver with the defined service and options
    driver = webdriver.Chrome(service=service, options=options)
    print("WebDriver initialized successfully.")
    return driver


# Loads configuration from a JSON file.
# Arguments:
# - config_file: Path to the configuration file (default: "config.json").
# Returns:
# - A dictionary containing the configuration parameters.
def load_config(config_file="assets/config.json"):
    with open(config_file, "r") as file:
        config = json.load(file)
    print("Configuration loaded successfully.")
    return config


# Reads URLs from a text file and returns them as a list.
# Arguments:
# - file_path: Path to the text file containing URLs.
# Returns:
# - A list of URLs.
def load_urls(file_path="urls.txt"):
    try:
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]  # Убираем пустые строки
        print(f"Loaded {len(urls)} URLs from '{file_path}'.")
        return urls
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return []


# Loads cookies from a file and applies them to the browser session.
# If the cookie file does not exist, prompts the user to run the cookie setup script.
# Arguments:
# - driver: Selenium WebDriver instance.
# - cookie_file: Path to the cookie file (default: "cookies.pkl").
def load_cookies(driver, url, cookie_file="assets/cookies.pkl"):
    if os.path.exists(cookie_file):
        print("Cookies file found. Loading cookies...")
        try:
            with open(cookie_file, "rb") as file:
                cookies = pickle.load(file)
            driver.get(url) 
            for cookie in cookies:
                if "domain" in cookie and cookie["domain"] not in url:
                    print(f"Skipping cookie due to domain mismatch: {cookie}")
                    continue
                driver.add_cookie(cookie)
            print("Cookies successfully loaded.")
            #driver.refresh()
        except (EOFError, pickle.UnpicklingError):
            print("Error: Cookies file is corrupted. Please run 'cookies.py' to save cookies again.")
            driver.quit()
            exit(1)
    else:
        print(f"Cookies file '{filename}' not found! Please run 'cookies.py' to save cookies.")
        driver.quit()
        exit(1)


# Loads names and emails from a CSV file and returns them as a list of dictionaries.
# Each dictionary contains name-email pairs from the CSV.
def load_names_and_emails(file_name="assets/names_and_emails.csv"):
    df = pd.read_csv(file_name)
    return df.to_dict(orient="records")


# Generates a random date within the last 2 months.
# Returns the date as a formatted string (YYYY-MM-DD).
def generate_random_date():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")


# Fetches reviews from the given product URL.
# This function navigates to the URL, opens the reviews modal, scrolls to load all reviews,
# and extracts the review content, rating, media, and user information.
def fetch_reviews(url, product_id, driver, names_and_emails):
    print(f"Opening page: {url}")
    driver.get(url)

    reviews = []
    try:
        print("Checking for 'View More' button...")

        # Attempt to find and click the 'View More' button up to 3 times
        for attempt in range(3):
            try:
                if driver.find_elements(By.CLASS_NAME, "comet-v2-btn-slim"):
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "comet-v2-btn-slim"))
                    ).click()
                    break
            except Exception as e:
                time.sleep(2)

        print("Waiting for the modal window to load...")
        modal_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "comet-v2-modal-body"))
        )
        time.sleep(2) 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class^='list--itemBox--']"))
        ) 
        print("Modal window loaded.")

        print("Scrolling to fully load all reviews...")
        prev_count = 0
        attempts = 0
        while True:
            review_elements = modal_body.find_elements(By.CSS_SELECTOR, "div[class^='list--itemBox--']")
            current_count = len(review_elements)

            if current_count > prev_count:
                prev_count = current_count
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal_body)
                time.sleep(2)
                attempts = 0
            else:
                attempts += 1
                if attempts >= 3:
                    print("All reviews loaded.")
                    break

        print("Collecting reviews...")
        for idx, element in enumerate(review_elements):
            try:
                review_text = element.find_element(By.CSS_SELECTOR, "div[class^='list--itemReview--']").text.strip()
                if len(review_text) < 20:
                    continue

                stars = len(element.find_elements(By.CSS_SELECTOR, "span.comet-icon-starreviewfilled"))
                if stars < 3:
                    continue

                media_elements = element.find_elements(By.CSS_SELECTOR, "div[class^='list--itemThumbnail--'] img")
                media_link = media_elements[0].get_attribute("src") if media_elements else ""

                user = random.choice(names_and_emails)
                reviews.append({
                    "review_content": review_text,
                    "review_score": stars,
                    "date": generate_random_date(),
                    "product_id": product_id,
                    "display_name": user["name"],
                    "email": user["email"],
                    "order_id": '',
                    "media": media_link,
                })
            except Exception as e:
                print(f"Error parsing review {idx + 1}: {e}")

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("output/error.png")
    return reviews

# Processes multiple URLs to fetch reviews and updates the CSV file after processing each URL.
def process_urls(urls, product_id, driver, names_and_emails, output_file="output/reviews.csv"):
    for url in urls:
        print(f"Processing URL: {url}")
        reviews = fetch_reviews(url, product_id, driver, names_and_emails)
        if reviews:
            file_exists = os.path.isfile(output_file)
            pd.DataFrame(reviews).to_csv(
                output_file, mode='a', index=False, header=not file_exists, encoding="utf-8"
            )
            print(f"Reviews from {url} saved to {output_file}.")
        else:
            print(f"No reviews found for {url}.")


# Main function to execute the review scraping process.
# It initializes the WebDriver, handles cookies, loads names and emails, fetches reviews, and saves them to a CSV file.
def main():
    config = load_config()
    urls = load_urls()
    product_id = 124123 #Айди продукта для изменения

    if not urls:
        print("No URLs found. Please add URLs to 'urls.txt'.")
        return
    
    driver = init_driver(config)
    load_cookies(driver, urls[0])
    try:
        names_and_emails = load_names_and_emails()
        process_urls(urls, product_id, driver, names_and_emails)
    finally:
        driver.quit()
        print("Script completed.")

if __name__ == "__main__":
    main()
