import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.tradingview.com/chart/?symbol=EURUSD"

def take_screenshot():
    # Folder create karein agar nahi hai
    folder = "screenshots"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Browser options for GitHub
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("Chart load ho raha hai...")
        driver.get(URL)
        time.sleep(35) # Indicators load hone ke liye thoda extra time
        
        # Naya filename (Date aur Time ke saath)
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M.png")
        file_path = os.path.join(folder, filename)
        
        driver.save_screenshot(file_path)
        print(f"Saved: {filename}")
        
        # Git Commands taake image GitHub par upload ho jaye
        os.system("git config --global user.name 'github-actions'")
        os.system("git config --global user.email 'github-actions@github.com'")
        os.system("git add .")
        os.system(f"git commit -m 'Chart Update: {filename}'")
        os.system("git push")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshot()
