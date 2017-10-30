"""
Created on Sun Oct 29 18:19:06 2017

INPUT:
    songList
    
OUTPUT:
    songList: a list of strings with song names
    
USAGE:
    songList = getHTML(link)

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

from functions import getHTML
from selenium import webdriver
import time
import os

songList = getHTML(input("Please enter the beatport top 100 link: "))

#Set directory
dir = os.path.dirname(os.path.realpath(__file__))
 
#Set extensions path
ext = os.path.join(dir, "chromeExt")
 
adblock = os.path.join(ext, "adblock.crx")
 
#Setting options
chop = webdriver.ChromeOptions()

chop.add_extension(adblock) #Extension
chop.add_argument("--mute-audio") #No audio, just in case
chop.add_experimental_option("prefs", {
  "download.default_directory": dir + "\Beatport Top 100",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
}) #Sets download location

#Setup browser driver with options
driver = webdriver.Chrome(chrome_options = chop)

driver.get("https://www.mp3juices.cc/")

#Run through each element in songList
for song in songList:
    
    searchBar = driver.find_element_by_id("query") #Find search bar
    
    searchBar.send_keys(song) #Type in song name
    
    driver.find_element_by_tag_name("button").click() #Click search
    
    time.sleep(1) #wait
    
    driver.find_element_by_link_text("Download").click() #Click download
    
    time.sleep(1) #wait
    
    driver.find_element_by_link_text("Download").click() #Again...
    
    searchBar.clear() #Clear search bar
          
driver.quit()
