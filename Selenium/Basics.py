from selenium import webdriver

# To not to show the Gui we use the options
from selenium.webdriver.chrome.options import Options

# Not to view the browser
chrome_options = Options()
chrome_options.add_argument("--headless")

# To get the chrome browser
driver = webdriver.Chrome(executable_path="C:\Webdrivers\chromedriver.exe", options=chrome_options)

# To request the website
driver.get('https://duckduckgo.com/')

# Find the element
search = driver.find_element_by_id("search_form_input_homepage")

# Type in the search bar
search.send_keys("My User agent")

# To click
btn = driver.find_element_by_id("search_button_homepage")
btn.click()

# To print the html code
print(driver.page_source)

# Every time close the driver
driver.close()
