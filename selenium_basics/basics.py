from selenium import webdriver
from shutil import which
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("detach", True)

chrome_path = which("chromedriver")

# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver = webdriver.Chrome(chrome_path, options=options)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get("https://duckduckgo.com/")

# driver.find_element(By.ID, "searchbox_input").send_keys("my user agent")
# driver.find_element(By.XPATH, "//button[contains(@class, 'searchbox_searchButton')]").click()

search_input = driver.find_element(By.ID, "searchbox_input")
search_input.send_keys("my user agent")
search_input.send_keys(Keys.ENTER)

# print(driver.page_source)

# driver.close()
