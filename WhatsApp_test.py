import time
from selenium import webdriver

chrome_browser = webdriver.Chrome(executable_path='C:/Users/Yetkin/Downloads/chromedriver_win32/chromedriver')
chrome_browser.get('https://web.whatsapp.com')

chrome_browser.implicitly_wait(15)
#input("QR kodu okuttuktan sonra Enter'a basın: ")

user_name = 'Refresh'
for_refresh = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))

#mssge = chrome_browser.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div[21]/div/div/div/div[1]/div/span[1]/span')
#print(mssge.text)

while True:
    
    if (chrome_browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/*/div/div/div[2]/div[2]/div[2]')):  
        unreadMsgs = chrome_browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/*/div/div/div[2]/div[2]')
        unreadMsgs.click()    
        

        message_box = chrome_browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        message_box.send_keys("Deneme")
        time.sleep(10)

        send_button = chrome_browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        send_button.click()
        time.sleep(10)

        for_refresh.click()
    else:
        pass