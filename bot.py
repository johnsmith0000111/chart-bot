import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.tradingview.com/chart/?symbol=EURUSD"

def take_screenshot():
    folder = "screenshots"
    if not os.path.exists(folder):
        os.makedirs(folder)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(URL)
        time.sleep(20) # Initial load
        
        # Hum 5 baar screenshot lenge har run mein (5 minutes total)
        # GitHub Actions ka ek session max 6 hours tak chal sakta hai
        for i in range(5): 
            filename = datetime.now().strftime("%H-%M-%S.png")
            file_path = os.path.join(folder, filename)
            
            driver.save_screenshot(file_path)
            print(f"Saved: {filename}")
            
            # Git commands to push immediately
            os.system("git config --global user.name 'github-actions'")
            os.system("git config --global user.email 'github-actions@github.com'")
            os.system("git add .")
            os.system(f"git commit -m 'Minute Update: {filename}'")
            os.system("git push")
            
            print("Waiting 60 seconds for next one...")
            time.sleep(60) # 1 minute ka wait
            driver.refresh() # Chart refresh karne ke liye
            time.sleep(15)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshot()
