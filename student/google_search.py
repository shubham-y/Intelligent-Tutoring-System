from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
print browser.current_url
driver.get('https://www.google.co.in/search')
# searchbox = driver.find_element_by_xpath("//input[@type='text']")
# searchbox.send_keys('Set theory')
# searchbutton = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]')
# # searchbutton.click()
# ActionChains(driver).move_to_element(searchbutton).click(searchbutton)