"""
Created on Sun Oct 29 18:19:06 2017

INPUT:
    A html link from a beatport top 100 playlist
    
OUTPUT:
    A folder in Desktop with the songs from the html link

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

from getHTML import getBeatport,getSpotify
from selenium import webdriver
from selenium.webdriver.remote.errorhandler import StaleElementReferenceException, NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os,sys
from sys import platform as _platform


print("""
==========================================
Welcome to the Beatport/spotify downloader
   
   Your link should consists of a table
   of songs on beatport or spotify
   
   Starting url examples:
   - www.beatport.com/label/
   - www.beatport.com/chart/
   - www.beatport.com/name/
   - www.beatport.com/release/
   - open.spotify.com/user/spotify/playlist/

 Please sort the files after downloading
 some could be corrupted or poor quality
(That's what we get for not buying songs)
=========================================""")

print("\n1. Spotify \n2. Beatport")
input_ = int(input("Please pick a platform: "))

if input_ == 1:
    songList,name = getSpotify(input("\nPlease enter the Spotify playlist link: "))
    platform = "Spotify"

elif input_ == 2:    
    songList,name = getBeatport(input("\nPlease enter the Beatport link: "))
    platform = "Beatport"
    
    
#Set directory
dir = os.path.dirname(os.path.realpath(sys.argv[0]))
 
#Set extensions path
ext = os.path.join(dir, "chromeExt")
adblock = os.path.join(ext, "adblock.crx")

#Crossplatform support
if _platform == "darwin":
    # MAC OS X
    cDriver = "/chromedriver" #Set chromedriver path
    desktop = os.path.expanduser("~/Desktop/{} {}".format(platform,name)) #Set download path
    
elif (_platform == "win32") or (_platform == "win64"):
    # Windows
    cDriver = "/chromedriver.exe" #Set chromedriver path
    desktop = os.path.expanduser("~\Desktop\{} {}".format(platform,name)) #Set download path

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

#Initial variables
failed = []
wait = 1

for song in songList:    
    try:
        print("Downloading: ",song)
        
        searchBar = driver.find_element_by_id("query") #Find search bar
        
        searchBar.send_keys(song) #Type in song name
        
        driver.find_element_by_tag_name("button").click() #Click search
        
        time.sleep(1) #Give script time to rest..
        
        #wait until we can click on download
        download1 = WebDriverWait(driver, wait).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.options")));
        
        download1.click();
        
        #wait until we can click on download
        while True:
            try:
                download2 = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.url")));
                
                download2.click();
                break
            
            #Try again            
            except TimeoutException:
                driver.refresh()
                
                searchBar = driver.find_element_by_id("query") #Find search bar
            
                searchBar.send_keys(song) #Type in song name
                
                driver.find_element_by_tag_name("button").click() #Click search
                
                #wait until we can click on download
                download1 = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.options")));
                
                download1.click();

        time.sleep(0.5)
        
        searchBar.clear() #Clear search bar
        
        #Check if stupid add tab opened
        if len(driver.window_handles)>1:
           tabs = driver.window_handles
           driver.switch_to_window(tabs[1])
           driver.close()
           driver.switch_to_window(tabs[0])
           
    except StaleElementReferenceException:
        driver.get("https://www.mp3juices.cc/")
        print("StaleElementException, Download failed, moving on")
        failed.append(song) 
        
    except NoSuchElementException:
        print("NoSuchElementException, Download failed, moving on")
        failed.append(song)
        searchBar.clear()
        
    except WebDriverException:
        print("WebDriverException, Download failed, moving on")
        failed.append(song)
        searchBar.clear()
    
print("\nFinished downloading songs!")

print("\nThe following songs failed:",failed)

input("Type anything to quit... \n")

driver.quit()
