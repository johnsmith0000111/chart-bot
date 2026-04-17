import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# TradingView URL
URL = "https://www.tradingview.com/chart/?symbol=EURUSD"

def take_screenshot():
    # Folder setup (Repository ke andar 'screenshots' naam ka folder)
    folder = "screenshots"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Browser Settings
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Chart load ho raha hai...")
        driver.get(URL)
        time.sleep(30) # Indicators load hone ka wait
        
        # Filename with Date and Time
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M.png")
        file_path = os.path.join(folder, filename)
        
        driver.save_screenshot(file_path)
        print(f"Screenshot save ho gaya: {file_path}")
    finally:
        driver.quit()

    # GitHub par Push karne ki commands
    os.system("git config --global user.name 'github-actions'")
    os.system("git config --global user.email 'github-actions@github.com'")
    os.system("git add .")
    os.system(f"git commit -m 'Auto-update chart: {filename}'")
    os.system("git push")

if __name__ == "__main__":
    take_screenshot()
