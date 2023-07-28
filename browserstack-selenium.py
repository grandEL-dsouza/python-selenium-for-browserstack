from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from threading import Thread

load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or "YOUR-USERNAME"
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or "YOUR-ACCESS-KEY"
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"
BUILD_NAME = "grandel test"
capabilities = [
    
    {
        "browserName": "Safari",
        "browserVersion": "13",
        "osVersion" : "Catalina",
        "os": "OS X ",   
        "sessionName": "grandel test",
        "buildName": BUILD_NAME,
        

    },
]
def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())
def run_session(cap):
    bstack_options = {
        "osVersion" : cap["osVersion"],
        "buildName" : cap["buildName"],
        "sessionName" : cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY,
    }
    if "os" in cap:
      bstack_options["os"] = cap["os"]
    options = get_browser_option(cap["browserName"].lower())
    if "browserVersion" in cap:
      options.browser_version = cap["browserVersion"]
    options.set_capability('bstack:options', bstack_options)
    driver = webdriver.Remote(
        command_executor=URL,
        options=options)
    try:
        driver.get("https://scholar.google.com/citations?user=3ykP4XkAAAAJ&hl=en")
        #driver.execute_script('browserstack_executor: {"action": "fileExists", "arguments": {"fileName": "InTouchPatientInstaller.pkg"}}')
        WebDriverWait(driver, 100)
        driver.get("https://www.xing.com/profile/Grandel_Dsouza/cv")
        driver.get("https://mu.academia.edu/GrandelDsouza")
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Sites loaded correctly"}}')
        WebDriverWait(driver, 100)
    except NoSuchElementException:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Some elements failed to load"}}')
    except Exception:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Some exception occurred"}}')
    # Stop the driver
    WebDriverWait(driver, 100)
    driver.quit()
for cap in capabilities:
  Thread(target=run_session, args=(cap,)).start()