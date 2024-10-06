from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()

# Get login credentials from environment variables
login_url = os.getenv('LOGIN_URL')
login_username = os.getenv('LOGIN_USERNAME')
login_password = os.getenv('LOGIN_PASSWORD')

# Debug: Print loaded credentials (be careful with passwords in logs)
logger.debug(f"Loaded URL: {login_url}")
logger.debug(f"Loaded username: {login_username}")
logger.debug(f"Loaded password: {'*' * len(login_password) if login_password else 'Not set'}")

# Path to your ChromeDriver
chrome_driver_path = '../drivers/chromedriver.exe'

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--verbose')
chrome_options.add_argument('--log-level=0')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.90 Safari/537.36')

# Set up Chrome service with the correct path to the driver
service = Service(executable_path=chrome_driver_path)

try:
    # Initialize the Chrome WebDriver with the options and service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logger.info("WebDriver initialized successfully")

    # Set an implicit wait
    driver.implicitly_wait(10)

    # Step 1: Open the website using the URL from the environment variable
    logger.info(f"Attempting to open URL: {login_url}")
    driver.get(login_url)
    logger.info("URL opened successfully")

    # Wait for the page to load completely
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Print the current URL and page source for debugging
    logger.debug(f"Current URL: {driver.current_url}")
    logger.debug(f"Page source: {driver.page_source[:1000]}...")  # Print first 1000 characters of page source

    # Step 2: Wait for the User ID field to be present before interacting with it
    try:
        # Try different selectors
        selectors = [
            (By.XPATH, "//input[@placeholder='User ID']"),
            (By.ID, "okta-signin-username"),
            (By.NAME, "username"),
            (By.XPATH, "//label[text()='User ID']/following-sibling::input"),
            (By.CSS_SELECTOR, "input[type='text']"),
        ]

        username_field = None
        for selector in selectors:
            try:
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(selector)
                )
                logger.info(f"User ID field found with selector: {selector}")
                break
            except TimeoutException:
                logger.warning(f"Selector {selector} not found")

        if username_field is None:
            raise NoSuchElementException("Unable to find User ID field with any selector")

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        logger.info("Password field found")

        # Step 3: Enter credentials
        if login_username and login_password:
            username_field.send_keys(login_username)
            password_field.send_keys(login_password)
            logger.info("Credentials entered")

            # Debug: Print the value entered in the username field
            entered_username = username_field.get_attribute('value')
            logger.debug(f"Entered username: {entered_username}")

            # Step 4: Click the 'Sign In' button
            sign_in_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Sign In']"))
            )
            sign_in_button.click()
            logger.info("Sign In button clicked")

            # Optional: Wait for login to complete
            WebDriverWait(driver, 20).until(EC.url_changes(login_url))
            logger.info(f"Login attempt completed. New URL: {driver.current_url}")

            # Add your code here to download the credit card statements
        else:
            logger.error("Login credentials not set in environment variables")

    except Exception as e:
        logger.error(f"Error during login process: {e}")
        logger.debug(f"Current URL: {driver.current_url}")
        logger.debug(f"Page source: {driver.page_source[:1000]}...")  # Print first 1000 characters of page source

except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
        logger.info("WebDriver closed")