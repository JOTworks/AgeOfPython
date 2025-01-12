import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pickle

# Set up Selenium
driver = webdriver.Chrome() 
driver.get("https://airef.github.io/commands/commands-index.html")

# Wait for a specific element to load (e.g., a div with class "content")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "command-name"))
    )
finally:
    # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    print("soup:")
    command_names = [c.text for c in soup.find_all(attrs={'class' : 'command-name'}, recursive=True)]
    
    # Save to a file
    with open('command_names.pkl', 'wb') as file:
      pickle.dump(command_names, file)

    driver.quit()

# Load from a file
with open('command_names.pkl', 'rb') as file:
    command_names = pickle.load(file)

print(len(command_names))  # Verify the content