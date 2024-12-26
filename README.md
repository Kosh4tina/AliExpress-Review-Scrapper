# AliExpress Review Scraper

This project is designed to scrape reviews from AliExpress using Selenium. The script is divided into two stages: manual cookie saving and automated review scraping.

---

## **Installation**

1. Make sure you have Python 3.8 or higher installed.
2. Install the required libraries:
   ```bash
   pip install selenium pandas
   ```
3. Download [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version and place it in the `assets` folder.

---

## **Project Structure**

```plaintext
project/
├── assets/
│   ├── chromedriver.exe         # Chrome WebDriver
│   ├── cookies.pkl              # Saved cookies
│   ├── names_and_emails.csv     # Data for review names and emails
├── output/
│   ├── reviews.csv              # Collected reviews
│   ├── error.png                # Screenshot of an error if it occurs
├── config.json                  # Configuration file
├── urls.txt                     # List of product URLs
├── cookies.py                   # Script for saving cookies
├── reviews.py                   # Script for scraping reviews
```

---

## **How to Use**

### 1. Set Up the Project
1. Edit `config.json` if needed:
   ```json
   {
     "browser": {
       "user_data_dir": "C:\\Users\\YourUser\\AppData\\Local\\Google\\Chrome\\User Data",
       "profile_directory": "Profile 3"
     },
     "cookies": {
       "file": "assets/cookies.pkl"
     },
     "url": "https://www.aliexpress.us"
   }
   ```
   - **user_data_dir**: Path to your Chrome user profile.
   - **profile_directory**: Specify the Chrome profile to use.

2. Add product URLs to `urls.txt` (one URL per line).

---

### 2. Save Cookies
1. Run `cookies.py`:
   ```bash
   python cookies.py
   ```
2. In the browser:
   - Select the shipping country (e.g., United States).
   - Solve any CAPTCHA presented.
   - Confirm in the console to save the cookies.
3. Cookies will be saved to `assets/cookies.pkl`.

---

### 3. Scrape Reviews
1. Ensure the `urls.txt` file is populated with product URLs.
2. Run `reviews.py`:
   ```bash
   python reviews.py
   ```
3. Collected reviews will be saved in `output/reviews.csv`.

---

## **Results**

### Example `reviews.csv` Output:
| review_content            | review_score | date       | display_name | email            | media |
|---------------------------|--------------|------------|--------------|------------------|-------|
| Great product!            | 5            | 2023-12-01 | Anonymous    | graxxx@gmail.com | N/A   |
| Took too long to arrive.  | 3            | 2023-11-20 | John         | johnxxx@yahoo.com| N/A   |

---

## **Common Errors**

- **InvalidCookieDomainException**:
  - Ensure that cookies were saved for the correct domain (`https://www.aliexpress.us`).
  - Re-run `cookies.py` to refresh the cookies.
- **Error Screenshots**:
  - If an error occurs during scraping, a screenshot will be saved in `output/error.png`.

---

## **Additional Notes**

1. Modify `names_and_emails.csv` to customize display names and emails for reviews.
2. The script automatically skips reviews shorter than 20 characters.

---

## **License**
This project is intended for personal use only. The author is not responsible for any violations of AliExpress terms of service.
