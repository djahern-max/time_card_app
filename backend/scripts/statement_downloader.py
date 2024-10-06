from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

# Initialize the WebDriver with options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Assume you're already logged in, and now navigate directly to the admin page
    driver.get("https://www.business.card.fnbo.com/accounts/admin")
    
    # Wait for the page to load and the "Download Transactions" button to be visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Download Transactions")))
    
    # Click the "Download Transactions" link
    download_link = driver.find_element(By.LINK_TEXT, "Download Transactions")
    download_link.click()

    print("Download Transactions link clicked successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # You can choose to close the browser or leave it open
    pass  # Keep the browser open for further steps





