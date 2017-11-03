# -*- coding: utf-8 -*-


import urllib
from bs4 import BeautifulSoup

def getBeatport(link):
    """
    Created on Sun Oct 29 17:24:49 2017
    
    INPUT:
        link: A fully valid link for a beatport link with a table of songs
        
    OUTPUT:
        songList: a list of strings with song names
        
    USAGE:
        songList = getBeatport(link)
    
    @Author: Simon Moe Sørensen, moe.simon@gmail.com
    """

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
    
    while True:
        #Genre from top 100
        try:
            name = soup.find(class_="interior-title")
            name = name.h1.string
            break
                  
        except AttributeError:
            pass
        
        #Label releases      
        try:
            name = soup.find(class_="interior-title")
            name = name.h1.string
            break
        
        except AttributeError:
            pass
        
        #Charts
        try:
            name = soup.find_all(class_="value")
            name = name[2].a.string
            break
        
        except AttributeError:
            pass
        
        except IndexError:
            pass
        
        #Releases
        try:
            name = soup.find(class_="interior-release-chart-content")
            name = name.h1.string
            break
        
        except AttributeError:
            pass
    
    #See if we have a "/"
    if name.find("/") != -1:
        name = name.replace(" /","")
        
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
        
    return songList,name

def getSpotify(link):
    """
    Created on Sun Oct 29 17:24:49 2017
    
    INPUT:
        link: A fully valid link for a spotify playlist
        
    OUTPUT:
        songList: a list of strings with song names
        
    USAGE:
        songList = getSpotify(link)
    
    @Author: Simon Moe Sørensen, moe.simon@gmail.com
    """

    #Initial list
    songList = []
    
    #Display for user
    print("\nPlease wait while the program initializes...")

    #Load the HTML data
    page = urllib.request.urlopen(link)

    #Store the HTML data in Beautiful soup format
    soup = BeautifulSoup(page, "lxml")
    
    #Get all song titles
    songInfo = soup.find_all(class_="tracklist-col name")
    
    name = soup.find(class_="entity-info")
    name = name.h1.string

    #See if we have a "/"
    if name.find("/") != -1:
        name = name.replace(" /","")
        
    #Run over i amount of songs and get their titles and artists
    for i in range(len(songInfo)):
        try:
            songTitle = songInfo[i].find(class_="track-name").string
            songArtist = songInfo[i].find("a").string
            
        except AttributeError:
            continue
        
        song = ' '.join((songArtist,songTitle))
        
        songList.append(song)
        
    return songList,name
    