"""
Created on Sun Oct 29 18:19:06 2017

INPUT:
    A html link from a beatport top 100 playlist
    
OUTPUT:
    A folder in Desktop with the songs from the html link

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

from getHTML import getHTML
from selenium import webdriver
from selenium.webdriver.remote.errorhandler import NoSuchElementException, WebDriverException
import time
import os,sys
from sys import platform as _platform


print("""
=========================================
   Welcome to the Beatport downloader

 Please sort the files after downloading
 some could be corrupted or poor quality
(That's what we get for not buying songs)
=========================================""")

songList,genre = getHTML(input("\nPlease enter the Beatport Top 100 link: "))

#Set directory
dir = os.path.dirname(os.path.realpath(sys.argv[0]))
 
#Set extensions path
ext = os.path.join(dir, "chromeExt")
adblock = os.path.join(ext, "adblock.crx")

#Crossplatform support
if _platform == "darwin":
    # MAC OS X
    cDriver = "/chromedriver" #Set chromedriver path
    desktop = os.path.expanduser("~/Desktop/Beatport {}".format(genre)) #Set download path
    
elif (_platform == "win32") or (_platform == "win64"):
    # Windows
    cDriver = "/chromedriver.exe" #Set chromedriver path
    desktop = os.path.expanduser("~\Desktop\Beatport {}".format(genre)) #Set download path

#Setting options
chop = webdriver.ChromeOptions()

chop.add_extension(adblock) #Extension
chop.add_argument("--mute-audio") #No audio, just in case
chop.add_experimental_option("prefs", {
  "download.default_directory": desktop,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
}) #Sets download location

   
#Setup browser driver with options
driver = webdriver.Chrome(ext+cDriver,chrome_options = chop)
driver.set_window_size(429,551)

driver.get("https://www.mp3juices.cc/")

#Remove extra tabs
tabs = driver.window_handles
driver.switch_to_window(tabs[1])
driver.close()
driver.switch_to_window(tabs[0])

#Run through each element in songList
for song in songList:
    
    try:
        print("Downloading: ",song)
        
        searchBar = driver.find_element_by_id("query") #Find search bar
        
        searchBar.send_keys(song) #Type in song name
        
        driver.find_element_by_tag_name("button").click() #Click search
        
        time.sleep(1.3) #wait
        
        driver.find_element_by_link_text("Download").click() #Click download
        
        time.sleep(1.3) #wait
        
        driver.find_element_by_link_text("Download").click() #Again...
        
        time.sleep(0.5)
        
        searchBar.clear() #Clear search bar
        
        #Check if stupid add tab opened
        if len(driver.window_handles)>1:
           tabs = driver.window_handles
           driver.switch_to_window(tabs[1])
           driver.close()
           driver.switch_to_window(tabs[0])
           
    except NoSuchElementException:
        print("Download failed, moving on")
        searchBar.clear()
        
    except WebDriverException:
        print("Download failed, moving on")
        searchBar.clear()
        
    
driver.quit()
