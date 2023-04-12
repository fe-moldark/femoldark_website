---
layout: default
title: Game Console
permalink: /game_console/
nav_order: 7
--- 

<head>
  <link rel="stylesheet" type="text/css" href="/styles/embedded_videos_and_stls.css">
</head>

# The Game Console
I thought it would be cool to design my own handheld console for this game, and despite some initial frustrations it has been fun to develop. Some neat aspects of this design:<br>
- There is a pop out button panel on the left side with buttons for starting my game directly, for starting the Retropie software, and two for shutting down and restarting the device
- Not only is there a battery pack so the game console is portable, but the battery also acts as a UPS for easy transitions between powering over USB-C and the battery
- Audio can be routed through two external speakers or to a 3.5mm audio jack using a manual DPDT 3-Pos switch
- Volume control is achieved using a potentiometer and a couple of gears
- The screen is 7", much larger than your typical handheld Retropie case from Adafruit allows for (no hate on them, I also have a case like this)
- Removable USB storage hidden away in a pop out section on the right side
- A fan to keep the computer cool
- Neat assembly / disassembly - I'll make a full video showing how this works later on

<br>
The game console can be divided into two main categories - the 3d-printed case and the electronic components inside.
<br><br>

## 3d model
Below is the center back piece only, the entire console is split up into several files which you can view on my Sketchfab account <a href="https://sketchfab.com/femoldark" target="_blank" rel="noopener noreferrer">here</a>. Here is that piece:<br>
<center>
  <div id="content"> 
    <iframe id="content" title="Game Console - Center Back Piece" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/f9cc6bdd460d491d8f15a5a79d7813e2/embed"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/game-console-center-back-piece-f9cc6bdd460d491d8f15a5a79d7813e2?utm_medium=embed&utm_campaign=share-popup&utm_content=f9cc6bdd460d491d8f15a5a79d7813e2" target="_blank" style="font-weight: bold; color: #1CAAD9;"> Game Console - Center Back Piece </a> by <a href="https://sketchfab.com/femoldark?utm_medium=embed&utm_campaign=share-popup&utm_content=f9cc6bdd460d491d8f15a5a79d7813e2" target="_blank" style="font-weight: bold; color: #1CAAD9;"> femoldark </a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=f9cc6bdd460d491d8f15a5a79d7813e2" target="_blank" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
  </div>
</center>
<br><br>

## Circuit Diagram
This is currently what the wiring for the game console looks like:<br>
<center>
  <img src="https://wesleykent.com/assets/circuit_diagram/gameconsole_circuit.png" alt="" width=1050><br>
</center>
<br><br>

## Electronic Components
This is not a complete list and it may very well change, but here is what I've been using so far:<br>
- <a href="https://www.adafruit.com/product/987" target="_blank" rel="noopener noreferrer">Stereo 3.7W Class D Audio Amplifier - MAX98306</a>
- <a href="https://www.adafruit.com/product/5270" target="_blank" rel="noopener noreferrer">Alpha Dual-Gang 16mm Right-angle PC Mount - 50K Audio - RV16A01F-41-15R1-A25K-30H4</a>
- <a href="https://www.adafruit.com/?q=resistors&p=5&sort=BestMatch" target="_blank" rel="noopener noreferrer">Some resistors (the ones I used for the LED were 220-330 Ohms, I believe)</a>
- <a href="https://www.adafruit.com/product/2934" target="_blank" rel="noopener noreferrer">2x PiGrrl Zero Custom Gamepad PCB</a>
- For the buttons I used a mix of <a href="https://www.adafruit.com/product/367" target="_blank" rel="noopener noreferrer">these</a>  and <a href="https://www.adafruit.com/product/3101" target="_blank" rel="noopener noreferrer">these</a> depending on purpose and preference
- <a href="https://www.adafruit.com/product/4202" target="_blank" rel="noopener noreferrer">Diffused 3mm LEDs</a>
- <a href="https://www.adafruit.com/product/1890" target="_blank" rel="noopener noreferrer">2x speakers </a>
- <a href="https://www.adafruit.com/product/1699" target="_blank" rel="noopener noreferrer">3.5mm audio jack</a>
- A 2-position DPDT switch <a href="https://raw.githubusercontent.com/fe-moldark/wesleykent-website/gh-pages/assets/circuit_diagram/DPDT_switch.png" target="_blank" rel="noopener noreferrer">that looks something like this</a>
- <a href="https://www.adafruit.com/product/805" target="_blank" rel="noopener noreferrer">2x SPST / SPDT switches</a>
- A RPi 4 or BPi M5 should both work
- Wires, solder, soldering iron, heat shrink tubing, perfboards / breadboards, wire cutters, etc.
<br><br><br>


I cover the game console's development more in depth on my personal website <a href="https://wesleykent.com/femoldark/gameconsole/" target="_blank" rel="noopener noreferrer">here</a>, <a href="https://wesleykent.com/femoldark/circuit_diagram/" target="_blank" rel="noopener noreferrer">here</a> and <a href="https://wesleykent.com/femoldark/stls_for_download/" target="_blank" rel="noopener noreferrer">here</a>.
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
