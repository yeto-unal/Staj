import time
from selenium import webdriver

chrome_browser = webdriver.Chrome(executable_path='C:/Users/Yetkin/Downloads/chromedriver_win32/chromedriver')
chrome_browser.get('https://web.whatsapp.com')

time.sleep(15)

while True:
    if(chrome_browser.find_elements_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[2]/div[2]/span[1]/div/span')):  
        user = chrome_browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[2]/div[2]/span[1]/div/span')
        user.click()

        message_box = chrome_browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        message_box.send_keys("Deneme")

        message_box = chrome_browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        message_box.click()

        for_refresh = chrome_browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[10]/div/div/div[2]')
        message_box.click()
    else:
        pass    

#//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[2]/div[2]/span[1]/div/span (gelene mesaj)
#//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/span/span