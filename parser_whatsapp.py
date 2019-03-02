import re
from selenium import webdriver
 
BASE_URL = "https://web.whatsapp.com/"
 
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
 
 
## EMOTI
def find_emoti(source_header):
    start_flag = 'data-plain-text="'
    end_flag = ' style='
    try:
        emoti_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return emoti_msg
    except Exception:
        return ''
 
## MENTION
def find_mention(source_header):
    start_flag = 'quoted-mention">'
    end_flag = '<'
    try:
        mention_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return mention_msg
    except Exception:
        return ''
 
## LINKS
def find_link(source_header):
    start_flag = '<a href="'
    end_flag = '"'
    try:
        link_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return link_msg
    except Exception:
        return ''
 
## IMAGE
def find_img(source_header):
    start_flag = '<img src="'
    end_flag = '"'
    try:
        img_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return img_msg
    except Exception:
        return ''
 
## FILE FROM
def find_file_from(source_header):
    start_flag = '_2a1Yw _1OmDL">'
    end_flag = '<'
    try:
        file_from_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return file_from_msg
    except Exception:
        return ''
 
## FILE TIME
def find_file_time(source_header):
    start_flag = '"_3EFt_">'
    end_flag = '<'
    try:
        file_time_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return file_time_msg
    except Exception:
        return ''
 
## RESENDED
def find_resended(source_header):
    start_flag = '_15aTv">'
    end_flag = '<'
    try:
        resended_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return resended_msg
    except Exception:
        return ''
 
## FROM
def find_from(source_header):
    start_flag = 'data-pre-plain-text="\['
    end_flag = ': '
    try:
        from_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return from_msg
    except Exception:
        return ''
 
## MSG CONTENT
def find_msg_content(source_header):
    start_flag = 'copyable-text">'
    end_flag = '</span>'
    try:
        content_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return content_msg
    except Exception:
        return ''
 
## AUDIO
def find_audio(source_header):
    start_flag = '<audio src="'
    end_flag = '"'
    try:
        content_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
        return content_msg
    except Exception:
        return ''
 
## PDF
def find_pdf_title(source_header):
    pdf_flag = 'icon-doc-pdf'
    if pdf_flag in source_header:
        start_flag = 'title="Descargar “'
        end_flag = '”"'
        try:
            content_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
            return content_msg
        except Exception:
            return ''
 
## PDF FROM
def find_pdf_from(source_header):
    pdf_flag = 'icon-doc-pdf'
    if pdf_flag in source_header:
        start_flag = 'class="RZ7GO" role="button">'
        end_flag = '</span>'
        try:
            content_msg = re.search(start_flag+'(.*?)'+end_flag, source_header).group(1)
            return content_msg
        except Exception:
            return ''
 
 
 
def play(driver):
 
    while True:
 
 
        #CLICK CHAT
        driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div[1]').click()
 
        num = input('NUM')
        #CONTENEDOR MENSAJES
        try:
            contenedor = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div['+num+']')
            source_header = contenedor.get_attribute('innerHTML')
 
            print('************************')
            print(source_header)
            print('************************')
 
            # CALL FUNCTIONS
            emoti = find_emoti(source_header)
            mention = find_mention(source_header)
            link = find_link(source_header)
            img = find_img(source_header)
            file_from = find_file_from(source_header)
            file_time = find_file_time(source_header)
            resended = find_resended(source_header)
            from_msg = find_from(source_header)
            content = find_msg_content(source_header)
            audio = find_audio(source_header)
            pdf_title = find_pdf_title(source_header)
            pdf_from = find_pdf_from(source_header)
 
            msg_array = []
            msg_array.append(emoti)
            msg_array.append(mention)
            msg_array.append(link)
            msg_array.append(img)
            msg_array.append(file_from)
            msg_array.append(file_time)
            msg_array.append(resended)
            msg_array.append(from_msg)
            msg_array.append(content)
            msg_array.append(audio)
            msg_array.append(pdf_title)
            msg_array.append(pdf_from)
 
            for e in msg_array:
                if e != '':
                    print(e)
        except Exception:
            print('NO NUMBER')
            continue
 
 
 
 
    driver.close()
 
 
play(login())
