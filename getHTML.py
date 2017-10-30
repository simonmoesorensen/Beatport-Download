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
from bs4 import BeautifulSoup

def getHTML(link):

    #Initial list
    songList = []
    
    #Display for user
    print("\nPlease wait while the program initializes...")

    #Load the HTML data
    page = urllib.request.urlopen(link)

    #Store the HTML data in Beautiful soup format
    soup = BeautifulSoup(page, "lxml")
    
    #Get all song titles
    songName = soup.find_all("p", class_="buk-track-title")
    songArtists = soup.find_all("p", class_="buk-track-artists")
    
    #Get genre
    genre = soup.find(class_="interior-title")
    genre = genre.h1.string
    
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
        
    return songList,genre
    
    