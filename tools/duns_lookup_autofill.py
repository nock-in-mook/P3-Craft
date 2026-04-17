# D-U-N-S Lookup auto-fill script (Selenium)
# Usage: py -3.14 tools/duns_lookup_autofill.py

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# --- .env load ---
env_path = Path(__file__).parent.parent / ".env"
env_vars = {}
with open(env_path, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            env_vars[key.strip()] = val.strip()

FIRST_NAME = env_vars.get("DUNS_FIRST_NAME", "")
LAST_NAME = env_vars.get("DUNS_LAST_NAME", "")
PHONE = env_vars.get("DUNS_PHONE", "")
PHONE_LOCAL = PHONE[1:] if PHONE.startswith("0") else PHONE

LEGAL_NAME = "P3 Craft"
STREET = "Shibuya Dogenzaka Tokyu Building 2F-C, 1-10-8 Dogenzaka"
CITY = "Shibuya-ku"
POSTAL = "150-0043"
EMAIL = "info@p3craft.com"

SELENIUM_PROFILE = str(Path(__file__).parent.parent / ".selenium-profile")
URL = "https://developer.apple.com/enroll/duns-lookup/"


def type_into(driver, element_id, value):
    """Clear field and type value using Selenium (most reliable)"""
    el = driver.find_element(By.ID, element_id)
    el.click()
    el.clear()
    el.send_keys(value)
    el.send_keys(Keys.TAB)
    print(f"[OK] #{element_id}: {value}")


def select_by_value(driver, element_id, value):
    """Select option using Selenium Select class"""
    el = driver.find_element(By.ID, element_id)
    sel = Select(el)
    sel.select_by_value(value)
    print(f"[OK] #{element_id}: {value}")


def select_by_text_contains(driver, element_id, text):
    """Select option whose visible text contains given text"""
    el = driver.find_element(By.ID, element_id)
    sel = Select(el)
    for opt in sel.options:
        if text in opt.text:
            sel.select_by_value(opt.get_attribute("value"))
            print(f"[OK] #{element_id}: {opt.text}")
            return
    print(f"[!!] #{element_id}: '{text}' not found")


def main():
    print("Starting Chrome (Selenium profile)...")
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={SELENIUM_PROFILE}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    # Wait for form
    print("Waiting for D-U-N-S form...")
    print("  -> If login page appears, log in with your Apple ID")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "countryCode"))
    )
    time.sleep(1)
    print("[OK] Form loaded!")

    # 1) Region -> Japan
    select_by_value(driver, "countryCode", "JP")

    # Wait for state/province options to load after country change
    print("Waiting for state options...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "headquartersAddressSubdivision"))
    )
    time.sleep(2)

    # 2) Legal Entity Name
    type_into(driver, "legalEntityName", LEGAL_NAME)

    # 3) Street
    type_into(driver, "headquartersAddressStreet", STREET)

    # 4) City
    type_into(driver, "headquartersAddressCity", CITY)

    # 5) State -> Tokyo
    select_by_text_contains(driver, "headquartersAddressSubdivision", "Tokyo")

    # 6) Postal Code
    type_into(driver, "headquartersAddressPostalCode", POSTAL)

    # 7) HQ Phone Country Code -> 81
    select_by_value(driver, "headquartersAddressPhoneCountryCode", "string:81")

    # 8) HQ Phone Number
    type_into(driver, "headquartersAddressPhoneNumber", PHONE_LOCAL)

    # 9) First Name
    type_into(driver, "workContactGivenName", FIRST_NAME)

    # 10) Last Name
    type_into(driver, "workContactFamilyName", LAST_NAME)

    # 11) Work Phone Country Code -> 81
    select_by_value(driver, "workContactPhoneCountryCode", "string:81")

    # 12) Work Phone Number
    type_into(driver, "workContactPhoneNumber", PHONE_LOCAL)

    # 13) Work Email
    type_into(driver, "workContactEmail", EMAIL)

    print()
    print("=== Auto-fill complete! ===")
    print("-> Enter CAPTCHA manually, then click Continue")
    print()
    print("Close the browser when done.")

    # Keep browser open
    try:
        while True:
            time.sleep(5)
            try:
                _ = driver.title
            except:
                break
    except KeyboardInterrupt:
        pass
    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    main()
