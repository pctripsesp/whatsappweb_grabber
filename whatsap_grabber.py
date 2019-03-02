import re
from selenium import webdriver
import time
import os
import datetime
 
 
date = str(datetime.datetime.now()).replace(' ','_')
BASE_URL = "https://web.whatsapp.com/"
WORKDIR = 'chats_' + date + '/'
 
def login():
 
    ## HEADLESS MODE SELECTION
    headless_mode = False
 
    if headless_mode:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        try:
            driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
        except:
            driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    else:
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
 
    driver.get(BASE_URL)
    input("SCAN QR CODE AND PRESS ANY KEY TO CONTINUE")
 
    return driver
 
 
 
def get_chats_info(driver):
 
    # GET NUMBER OF CHATS (WE MUST ADD 1 TO THAT NUMBER)
    e = driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div[1]')
    source_numberChats = e.get_attribute('style')
    start_flag_numberChats = 'z-index: '
    end_flag_numberChats = ';'
    number_of_chats = int(re.search(start_flag_numberChats+'(.*?)'+end_flag_numberChats,source_numberChats).group(1))+1
    print('NUMBER OF CHATS -->', number_of_chats)
 
    # LOOP TO GET ALL CHATS INFO (WEBWHATSAPP LIMITS VIEW FROM 19 TO 21 CHATS ONLY), THEN REASIGNS NUMBERS
    get_chat_content(driver, 1, 1)
    time.sleep(10)
    chat_number = 1
    flag_chats = True
    while flag_chats:
        for element_number in reversed(range(1,21)):
            chat_number+=1
            get_chat_content(driver, element_number, chat_number)
            if chat_number == number_of_chats+1:
                flag_chats = False
                break
 
 
def get_chat_content(driver, element_number, chat_number):
 
    # CLICK CHAT (WE NEED TO WAIT REFRESH, USE TRY LOOP UNTIL PAGE IS LOADED)
    near_end_counter = 1
    flag_near_end = True
    while flag_near_end:
        try:
            #print('TRYING',element_number)
            driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div['+str(element_number)+']').click()
            element_header = driver.find_element_by_xpath('//*[@id="main"]/header')
            source_header = element_header.get_attribute('innerHTML')
            start_flag_name = 'title="'
            end_flag_name = '"'
            chat_name = re.search(start_flag_name+'(.*?)'+end_flag_name,source_header).group(1)
            print(str(chat_number) + ' --->'+'('+str(element_number)+')', chat_name)
 
            ## CREATE CHAT DIR
            if not os.path.exists(WORKDIR+chat_name+'/'):
                os.makedirs(WORKDIR+chat_name+'/'+'chat_screenshots/')
 
            ## IMG
            try:
                element_header_img = driver.find_element_by_xpath('//*[@id="main"]/header/div[1]/div/img')
                chat_img_URL = element_header_img.get_attribute('src')
                chat_img_URL = chat_img_URL.replace('dyn.', '')
                # DOWNLOAD IMG
                download_img(driver, chat_img_URL, chat_name)
            except Exception as e:
                # NO IMAGE ERROR
                if 'img' in str(e):
                    flag_near_end = False
                    print('IMAGE ERROR: NO IMAGE')
           
           
            ## CHAT MEMBERS
            '''
           try:
               element_members = driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[2]')
               chat_members = element_members.get_attribute('innerHTML')
           except Exception as members_error:
               print('MEMBERS', members_error)
           '''
 
            ## SAVE ALL CHAT HISTORY
            save_msgs(driver, chat_name)
 
            near_end_counter = 1
 
        except Exception as e:
            # ELEMENT 20 ERROR
            if '"//*[@id="pane-side"]/div/div/div/div[20]"' in str(e):
                flag_near_end = False
                print('ELEMENT ERROR: NO 20 ELEMENT')
                continue
            print(e)
            time.sleep(2)
            near_end_counter += 1
            # WHEN NEAR END OF CHATS, MAX NUMBER OF ELEMENT CAN CHANGE FROM 20 TO 19
            ## WE DISCARD 20
            if near_end_counter > 3:
                flag_near_end = False
            continue
        break
 
 
########################
## AUXILIAR FUNCTIONS ##
########################
# DOWNLOAD PROFILE/CHAT IMG
def download_img(driver, chat_img_URL, chat_name):
    # OPEN NEW TAB, DOWNLOAD IMG AND CLOSE TAB
    str_url = "window.open('"+chat_img_URL+"', 'new_window')"
    driver.execute_script(str_url)
    driver.switch_to.window('new_window')
    driver.save_screenshot(WORKDIR+chat_name+'/'+chat_name+".png")
    driver.execute_script("window.close('new_window')")
    driver.switch_to.window(driver.window_handles[0])
 
# SCROLLS, SAVES TEXT AND SCREENSHOTS OF A CHAT
def save_msgs(driver, chat_name):
    c = 1
    final = 0
    flag_final = False
    screenshot_num = 1
    while not flag_final:
        try:
            listOfmsgs = driver.find_elements_by_xpath("//div[contains(@class, 'vW7d1')]")
            #upper_msg = driver.find_element_by_xpath("//div[contains(@class, 'vW7d1')]")
 
            print('MSG', c, '/', len(listOfmsgs))
            if c > (len(listOfmsgs)-3):
                c = len(listOfmsgs)
            else:
                c+=2
            if c == len(listOfmsgs):
                final += 1
                time.sleep(5)
                if final == 5:
                    print('END OF CHAT')
                    flag_final = True
                    break
            else:
                final = 0
            try:
                # SCROLL
                driver.execute_script("arguments[0].scrollIntoView();", listOfmsgs[-c])
                # TAKE SCREENSHOT
                driver.save_screenshot(WORKDIR+chat_name+'/'+'chat_screenshots/'+chat_name+'_'+str(screenshot_num)+".png")
                screenshot_num+=1
 
            except Exception as err:
                print(err)
                c = len(listOfmsgs)
                time.sleep(3)
                continue
            time.sleep(0.5)
 
        except Exception as e:
            print(e)
            continue
 
 
login = login()
get_chats_info(login)
