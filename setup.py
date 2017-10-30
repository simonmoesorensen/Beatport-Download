# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 17:04:20 2017

A setup script that creates an .exe file of the project inside the "build" folder

USAGE:
    From terminal or cmd, write:
        python setup.py bdist_msi <- for windows installer
        python setup.py bdist_mac <- for mac installer (only works if run from on mac os)

@author: Simon Moe Sørensen, moe.simon@gmail.com
"""

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
additional_mods = ["bs4.tests.test_builder_registry","bs4.tests.test_lxml","bs4.tests.test_soup"]

include_files = ["chromeExt/"]

packages = ["getHTML","selenium","time","os","bs4","lxml","sys"]

build_exe_options = {"packages": packages, "excludes": ["tkinter"], 
                     "includes":additional_mods, "include_files":include_files}



base = None

setup(  name = "Beatport Top 100 Downloader",
        version = "1.0",
        author = "Simon Moe Sørensen",
        description = "This programs downloads a given top 100 beatport list",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
