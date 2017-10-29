# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 17:24:49 2017

INPUT:
    link: A fully valid link for a top-100 url from beatport
    
OUTPUT:
    songList: a list of strings with song names
    
USAGE:
    songList = getHTML(link)

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

import urllib
from bs4 import BeautifulSoup, SoupStrainer

def getHTML(link):
    
    #Initial list
    songList = []

    #Load the HTML data
    page = urllib.request.urlopen(link)
    
    #Store the HTML data in Beautiful soup format
    soup = BeautifulSoup(page, "lxml")
    
    #Get all song titles
    songName = soup.find_all("p", class_="buk-track-title")
    songArtists = soup.find_all("p", class_="buk-track-artists")
    
    #Run over i amount of songs and get their titles and artists
    for i in range(len(songName)):
        try:
            songTitle = songName[i].find(class_="buk-track-primary-title").string
            songRemix = songName[i].find(class_="buk-track-remixed").string
            songArtist = songArtists[i].find("a").string
            
        except AttributeError:
            continue
        
        song = ' '.join((songArtist,songTitle,songRemix))
        
        songList.append(song)
        
    return songList

"""
Created on Sun Oct 29 23:00:19 2017

INPUT:
    
OUTPUT:
    
USAGE:
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""
from urllib.request import HTTPError

from pytube import YouTube

def getUrl(songList):
    
    for song in songList:
        #Convert song name from songList into query form
        query = urllib.request.quote(song)
        
        #Define the search url
        url = "https://www.youtube.com/results?search_query=" + query
        
        #Find video and download
        try:
            response = urllib.request.urlopen(url)
            
            html = response.read()
            
            soup=BeautifulSoup(html,"lxml",parse_only=SoupStrainer('a'))
            
            vid = soup.find(attrs={'class':'yt-uix-tile-link'})
            
            url = ('https://www.youtube.com' + vid['href'])
            
            print("Downloading: ",song)
            
            YouTube(url).streams.filter(only_audio=True).first().download()
        
        #Stop if google banned us
        except HTTPError: 
            print("Google banned us...")
            break
    
    
    
    
    