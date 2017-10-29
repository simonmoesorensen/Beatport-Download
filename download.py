# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 23:22:05 2017

INPUT:
    
OUTPUT:
    
USAGE:
    

@Author: Simon Moe Sørensen, moe.simon@gmail.com
"""

from functions import getHTML,getUrl

link = input("Please enter the beatport top 100 website: ")

songList = getHTML(link)

urlList = getUrl(songList)