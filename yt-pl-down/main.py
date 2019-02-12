#!/usr/bin/env python3


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time



# <CHROME INIT>
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs", prefs)
options.binary_location = r"/usr/bin/chromium-browser"
driver = webdriver.Chrome(chrome_options=options)
# </CHROME INIT>


# replace this link with your own
link = "https://www.youtube.com/playlist?list=PLyfV9MvIdnbaNQRKx5Lv95wDXYofI5jfW"



def getLinks(link):
    print("Retrieving links..")
    
    file = open("links.txt", "w+")
    driver.get(link)
    time.sleep(3)

    linkelems = driver.find_elements_by_css_selector("#contents .yt-simple-endpoint")
    progress = 1

    for linkelem in linkelems:
            link = linkelem.get_attribute("href") + "\n"
            print("Writing link..")
            print(progress, "/", len(linkelems))
            
            file.write(link)
            progress += 1


    file.close()

def filterLinks():
    file = open("links.txt", "r")
    newLinks = open("newLinks.txt", "w+")

    links = file.readlines()
    prevlink = "stuff"

    for link in links:
        if ("/watch" in link and prevlink not in link):
            newLinks.write(link)
        prevlink = link

    newLinks.close()
    file.close()

def download():
    file = open("newLinks.txt")
    file = file.readlines()

    progress = 1
    length = str(len(file))
    print(length)

    for link in file:
        driver.get("http://convert2mp3.net/en/")

        
        print("Converting ", progress, "/", length)

        # Try to search for the yt video
        # Make sure the page is loaded
        while True:
            try:
                elem = driver.find_element_by_id("urlinput")
                elem.send_keys(link)
                break
            except:
                time.sleep(10)


        # Make sure no error message is present onsite
        while True:
            try:
                driver.find_element_by_class_name("alert-error")
                print("This video doesn't exist")
                print("Skipping..")
                break
            except NoSuchElementException: # No error is present, continue
                # Wait for the video to convert
                time.sleep(10)


                # Confirm current song tags on next screen
                while True:
                    try:
                        elem = driver.find_element_by_class_name("btn-success")
                        elem.click()
                        break
                    except:
                        time.sleep(10)

                # Wait for page to load
                time.sleep(5)

                print("Downloading ", progress, "/", length)

                # Press "Download" button and download the song
                while True:
                    try:
                        elem = driver.find_element_by_class_name("btn-success")
                        elem.click()
                        break
                    except:
                        time.sleep(10)
                break
            
        progress += 1
        time.sleep(5)
    print("Done! Downloaded ", progress, " files.")

    file.close()
    driver.quit()
        


getLinks(link)
filterLinks()
download()
