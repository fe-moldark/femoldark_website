---
layout: default
title: Downloading Scripts, Files and Folders
permalink: /downloading_scripts_files_and_folders/
nav_order: 3
---

# Downloading Scripts, Files and Folders
This page will cover how to download everything, where to download it to, what modules you will need, and more. To start off, just know this page only covers the Create Chapter program since I still need to rework the actual game script and its libraries.
<br><br>
The easiest way to download all of the files and folders you will need is to directly download the entire repository from <a href="https://github.com/fe-moldark/femoldark_website/archive/refs/heads/main.zip" target="_blank" rel="noopener noreferrer">here</a>. It will give you more than you need, but this ensures everything I add later on will still be accessible even as files, folders, and images change.
<br><br>
The following directories should be installed right into the Python3 home folder when on Windows or the home directory of the user if on Linux:
- The most current `/pics/` directory located in the `All-Images` folder from the above download
  - This contains subdirectories for the various tiles, background graphics, and character images
- The same applies to the latest `/FIRE_EMBLEM_SAVE_FILES/` directory, which can be found in `Full-folder-and-file-structure-uploads` in that same download. Remove whatever date is attached to the end of its name leaving just `/FIRE_EMBLEM_SAVE_FILES/`
<br><br>

# The Create Chapter Program
This is designed to work on Windows 10/11, but if you want to modify it to work on Linux then go for it. I did emulate a fresh Windows 11 VM and ensured everything worked as expected (but please let me know if something stops working). First of all, download the latest version of the program from <a href="https://github.com/fe-moldark/femoldark_website/tree/main/CreateChapterProgram" target="_blank" rel="noopener noreferrer">this directory</a>.
<br><br>
## _What else is needed:_
- Python3 from <a href="https://python.org/downloads/" target="_blank" rel="noopener noreferrer">here</a>. From that link find the latest stable release and choose the install for Windows option
- Pip should install alongside that, but if not you can download it separately. To confirm if it was downloaded enter `pip --version` at the command prompt
- Install the following modules with the `pip install <module name>` command: `pygame`, `xlrd`, `numpy`, and `matplotlib`


## _Working versions of these modules:_
Since I don't know if any future updates will mess things up, here are the current versions of all the modules I am using without issue:
- Pygame: 2.3.0
- Xlrd: 2.0.1
- Numpy: 1.24.2
- Matplotlib: this will install a host of other libraries...
- Python3 - 3.10.11
- Pip - 23.0.1
<br>

**Note: You can check what module versions you have installed using `pip freeze` at the command prompt.**
<br><br>

# FE Moldark
As stated, this part needs work and I will update as soon as I can. In the meantime, enjoy this Gif of happy Obi-Wan:<br>
<center>
<div class="tenor-gif-embed" data-postid="10168701" data-share-method="host" data-aspect-ratio="1.91803" data-width="75%"><a href="https://tenor.com/view/happy-starwars-obi-wan-kenobi-gif-10168701">Happy Starwars GIF</a>from <a href="https://tenor.com/search/happy-gifs">Happy GIFs</a></div> <script type="text/javascript" async src="https://tenor.com/embed.js"></script>
</center>
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
