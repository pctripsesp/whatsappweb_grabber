# Whatsapp Web Grabber
This is a simple script to grab all the information from a new web whatsapp session, using selenium and Chrome webdriver.


## Getting Started
Dependencies
```
sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4
sudo apt-get install default-jdk 
sudo apt-get install chromium-chromedriver
sudo apt-get install python3-pip
sudo pip3 install selenium

METHOD 2
wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```
Starting
```
git clone https://github.com/pctripsesp/whatsappweb_grabber.git
cd whatsappweb_grabber
python3 whatsap_grabber.py
```



### TODAY
- Open new Whatsapp Web session
- Open, scrolls and takes screenshot of all chats/groups
- Saves all screenshots in a directory with chat's name
- Saves profile picture of chat/group

### TODO

- Get contacts from each group
- Get all chat/group information like creation date, description...
- Parse and save in readable way all kind of information from chats like photos, videos, links, files... (working with parser_whatsapp.py file)


### LICENSE
#### Creative Commons NonCommercial
Not primarily intended for or directed towards commercial advantage or monetary compensation
