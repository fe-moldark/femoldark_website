---
title: File Formats
layout: default
permalink: /file_formats/
nav_order: 4
---

# File formats
{: .no_toc }
This page will cover different types of files and how they are formatted. Note that the [Create Chapter](/creating_chapters/) program I wrote already manipulates the files in the same format you'll see here, so you should only ever need to reference the actual files when debugging or just to better understand how everything is written. Also note that some of these formats will change and one or two I have already rewritten but have yet to be implemented in either the game or the Create Chapter program. Let's begin:
<br><br>

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta}
  
- TOC
{:toc}
</details>


## The Map file
Let's start with the map itself, the file is named `MAP.txt` within each level's main directory. Here is how a single row of the map is saved in text format:<br>
`[('chest1b.png', 0), ('grass_5.png', 0), ('roof_half2.png', 0),...]`
<br><br>
The three dots there indicate there is more to that row of course. How this ends up working is it will create an array based on the number of lines within the file (y) and the number of individual tiles within each row (x). From there, it loads the image according to the string part of the tile and the second part controls the rotation of that tile. Later on, two 0/1 grids are generated to control unit movement, one is for units on foot and the other for units that can fly. If I could go back in time and reformat how this was done, I would, but it works fine as is so you won't see me complaining.
<br><br><br>

## The Extra file
The `EXTRA.txt` file contains information pertaining to the chapter number, name, and background (water or lava). This file is similarly stored under each level's main directory. That might look something like:<br>
```
4
Village Strike
TurnLimit:False:0
Water
```
<br>
So, this would be chapter 4, "Village Strike" with water as its background for any tiles that require it, and no turn limit. If the "TurnLimit" were `True` and had a number higher than 0, this would indicate that whatever the win condition (which I am about to cover), that must be accomplished within the given number of turns. Think of the win condition for surviving `x` number of turns, this is the opposite side of that coin.
<br><br><br>

## Win Conditions
The last file under the parent level directory is the `WINCONDITIONS.txt` file, you can guess what it controls. This file can be structured in several different ways, which of course depends on what win condition has been set for the chapter. There are a total of six which I will explain and then show a brief example of how it needs to be formatted.
<br>
### 1. ROUT
{: .no_toc}
The simplest one is a rout mission, which means the player must eliminate all enemy forces on the map to move onto the next level. This is saved with only a single line to the file:<br>
```
ROUT
```
This is the only condition that only requires one line.
<br>

### 2. SEIZE
{: .no_toc}
A very common win condition is dependent on "seizing" a tile, most often occupied by that chapter's final boss unit who will not be removed from the tile until defeated. The seize condition is formatted as the following:<br>
```
SEIZE
X
Y
```
With X and Y denoting the location on the map.
<br>

### 3. ESCAPE
{: .no_toc}
This win condition is the exact same as the `SEIZE` option except for swapping out the first line for `ESCAPE`, and then followed by a location. Both have the same win conditions, but one is focused on capturing a location while the other is focused on escaping to another area.
<br>

### 4. SURVIVE
{: .no_toc}
This win condition is as simple as two lines:<br>
```
SURVIVE
#
```
The number tells you how many turns you must survive for, think of this as outlasting waves of enemy soldiers until reinforcements arrive or you are able to escape.
<br>

### 5. PROTECT
{: .no_toc}
This win condition is a simple requirement to protect an individual on the map, either a friendly or neutral unit. If you think about it, this actually applies to every chapter for the main character.<br>
```
PROTECT
Name
```
As soon as this condition is no longer met (i.e. the unit no longer exists on the map) you have failed the chapter.
<br>

### 6. KILL
{: .no_toc}
This is the opposite of the above statement, instead of protecting a friendly / neutral unit your mission is to kill a particular enemy unit, most often seen as "Defeat the boss". This can be used almost interchangeably with seizing, for instance a throne that the final boss occupies. That formats looks like the following:<br>
```
KILL
Name
```
<br>
_Note: On top of all these win conditions, the user can also assign a maximum number of turns the chapter must be completed by._
<br><br><br>

## Chests
Chest files are saved as:
```
Closed
X
Y
Loot name
```
That first line is depreciated, it was an old way I had of dealing with chests, now it just defaults to "Closed" for compatibility. Lines two and three denote its X and Y coordinates, and the fourth line is the loot. Nothing else is needed about the item or weapon as it will pull the rest of the information from a spreadsheet. Think the number of uses, max uses, worth, etc.
<br><br><br>

## Villages
A village save file might appear as the following:<br>
```
NOTVISITED
X
Y
villager.png
item;Darik Reserve (S)
Villager: NOT USING THIS LINE - BUT KEEP TO LOAD CORRECTLY
Villager: What's up bud? 
: I'm robbing you.
Villager: Damn, okay take all our money.
```
The first line there is yet another thing that is depreciated, don't worry about it. The X and Y mark the spot, the fourth line is the image of whoever is speaking. The fifth line is whatever loot is at the village. This is saved as either `item;item_name` for an item / weapon or as `unit;unit_name` for a new recruit. If it is simply `item;` then there is only a conversation, no reward. The following line, line 6, is ignored and everything after that is the conversation that will take place between the person at that village and the unit that visits. Everywhere there is only a `:` and no name, this means that it will fill in with whoever is visiting the village.
<br><br><br>

## Recruitable units
These are saved in two separate files, the first is a simple

```
Recruit Name
Recruiter1 Name
Recruiter2 Name
Recruiter3 Name
```
Only one name after the recruit is necessary, but you can add as many recruiters as you want for that recruit. Normally this list will never be longer than 1-3 friendly units.
<br><br>
This format is also changing since before there was only one conversation that could be had, now there will be different ones depending on who is talking. I will update this once I have rewritten how that works.
<br><br><br>



## Folder structure
You can view all of this yourself if you download the entire folder structure as described [here](/downloading_scripts_files_and_folders/), otherwise I will briefly cover it down below.
<br><br>

Under the main `FIRE_EMBLEM_SAVE_FILES` directory you should see something similar to this:<br>
<center>
  <img src="/assets/file_folder_structure/main_dir.png" alt="" width=900>
</center>
<br>
Brief explanation:
- The `_NEWGAME` folder contains some default settings, how much money and which units you begin with
- Any of the `SAVESLOTS` listed there contain a save file. This includes information like money, which units survived from the previous chapter, their inventories, etc. The only difference with the `SUSPENDPOINT` save file is that it contains information relevant to a mid-game save, including:
  - Entire unit data for friendly and enemy units (they may have traded items, lost health, be affected by poison, etc)
  - A list of which friendly units have already moved that turn
  - A list of which units (friendly and enemy) have died
  - Any changes to the map, including any chests or doors that have been opened, villages visited, etc.
  - If there are armories and vendors then noting how many of their wares are still available
  - Have any settings been changed such as volume, grid thickness, etc.
  - Have any new items or weapons been added to the convoy mid-game
  - _I'm probably missing one or two things, but you get the idea._
- The `SUPPLEMENTARY FILES` folder contains subdirectories for all potential ally units for when they are eventually introduced, as well as a `COMMON_MAPS` folder for chapters that will use the map on more than once occasion during conversations between units or cutscenes
- There are a few more files and folders but those will be changing, so I will update this in time
<br><br>

Just to quickly showcase how one chapter breaks down, here is what one of the levels within the `_ALLMAPS` directory looks like:<br>
<center>
  <img src="/assets/file_folder_structure/level_dir.png" alt="" width=900>
</center>
<br>
Everything outside of the 1,2 and 4 conversation folders is self-explanatory, and those three folders are a part of some upcoming reformatting I'm doing anyway.
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
