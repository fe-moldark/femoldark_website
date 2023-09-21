---
layout: default
title: Game Console
permalink: /game_console/
nav_order: 9
--- 

<head>
  <link rel="stylesheet" type="text/css" href="/styles/embedded_videos_and_stls.css">
</head>

# The Game Console
I thought it would be cool to design my own handheld console for this game, and despite some initial frustrations it has been fun to develop. Some neat aspects of this design:<br>
- There is a pop out button panel on the left side with buttons for starting my game directly, for starting a media center to play locally stored videos, and two others for shutting the device off and to turn the wireless interface up or down
- Not only is there a battery pack so the game console is portable, but the battery also acts as a UPS for seamless transitions between powering the console over USB-C and the battery
- Audio can be routed through two external speakers or to a 3.5mm audio jack using a manual 3-Pos DPDT switch
- Volume control is achieved using a dual-gang 5k potentiometer and a couple of gears
- The screen is 7", much larger than your typical handheld Retropie case from Adafruit allows for (no hate on them, I also have a case like this)
- There is a removable SD card in a pop out panel on the right side which has the RetroPie OS and some games installed (there were issues getting it installed as an application)
- A fan to keep the computer cool
- Neat assembly / disassembly that requires no unsoldering to get to the guts of the game console
- You can swap out an analog joystick with a d-pad in under a minute if you want

<br>
I cover the game console's development more in depth on my personal website <a href="https://wesleykent.com/femoldark/gameconsole/" target="_blank" rel="noopener noreferrer">here</a>. That discusses everything from assembling the hardware to configuring the software. If you want to see how the game console was developed I've recorded those on my <a href="https://www.youtube.com/playlist?list=PLecUQNqdK8lTFV4D1MFUgDr6TgxQrbloh" target="_blank" rel="noopener noreferrer">YouTube channel</a>. To give a brief overview, the game console can be divided into two main categories - the 3d-printed case and the electronic components inside:
<br><br>

## 3d model
If you want to view these all in a single webpage I have put them on display <a href="https://wesleykent.com/femoldark/stls_for_download/" target="_blank" rel="noopener noreferrer">here</a>. Otherwise you can view and download them from my <a href="https://sketchfab.com/femoldark" target="_blank" rel="noopener noreferrer">Skethfab account</a> or from this <a href="https://github.com/fe-moldark/wesleykent-website/tree/gh-pages/assets/3d_files/FinalGameConsole" target="_blank" rel="noopener noreferrer">Github repository</a>. There are 71 total pieces that I needed to design and print off, so a lot of effort went into this design.
<br><br>

## Circuit Diagram
This is what the final circuit diagram for the game console looks like:<br>
<center>
  <img src="/assets/updated_circuitv2.png" alt="" width=1050><br>
</center>
<br><br>

## Electronic Components
_*Goes without saying but none of this is sponsored, this is just where I happened to source the parts for this project from. If you can find these pieces cheaper elsewhere, go for it._
<br><br>
- <a href="https://www.adafruit.com/product/4296" target="_blank" rel="noopener noreferrer">1x Raspberry Pi 4 Model B (4 GB Ram)</a>
- <a href="https://www.waveshare.com/wiki/UPS_HAT_(B)" target="_blank" rel="noopener noreferrer">1x Waveshare UPS HAT (B)</a> and 2x 18650 batteries
- <a href="https://www.waveshare.com/7inch-hdmi-lcd-c.htm" target="_blank" rel="noopener noreferrer">1x 7" LCD</a>
- <a href="https://www.adafruit.com/product/987" target="_blank" rel="noopener noreferrer">1x Stereo 3.7W Class D Audio Amplifier - MAX98306</a>
- <a href="https://www.adafruit.com/product/5284" target="_blank" rel="noopener noreferrer">1x Alpha Dual-Gang 16mm Right-angle PC Mount - 5K Audio</a>
- <a href="https://www.adafruit.com/?q=resistors&p=5&sort=BestMatch" target="_blank" rel="noopener noreferrer">4x 220 Ohm and 1x 10K Ohm Resistors</a>
- <a href="https://www.adafruit.com/product/4202" target="_blank" rel="noopener noreferrer">4x Diffused 3mm LEDs</a>
- <a href="https://www.amazon.com/DEVMO-Joystick-Breakout-Controller-Arduino/dp/B07R7736QH" target="_blank" rel="noopener noreferrer">1x Analog 2-axis joystick</a> (This one should work, I got mine from a sensor module kit 4+ years ago)
- <a href="https://www.adafruit.com/product/856" target="_blank" rel="noopener noreferrer">1x MCP3008 Analog-to-Digital converter</a>
- <a href="https://www.adafruit.com/product/2934" target="_blank" rel="noopener noreferrer">2x PiGrrl Zero Custom Gamepad PCB</a>
- A mixture of <a href="https://www.adafruit.com/product/367" target="_blank" rel="noopener noreferrer">these</a>, <a href="https://www.adafruit.com/product/3101" target="_blank" rel="noopener noreferrer">these</a> and <a href="https://www.adafruit.com/product/4183" target="_blank" rel="noopener noreferrer">these</a> buttons depending on purpose and preference (overall 13 buttons are needed)
- <a href="https://www.aliexpress.us/item/3256803509242744.html" target="_blank" rel="noopener noreferrer">3x speakers</a> (yes, three)
- <a href="https://www.adafruit.com/product/1699" target="_blank" rel="noopener noreferrer">1x 3.5mm audio jack breakout board</a>
- <a href="https://www.adafruit.com/product/2222" target="_blank" rel="noopener noreferrer">1x Female GPIO Header</a> and <a href="https://www.adafruit.com/product/2822" target="_blank" rel="noopener noreferrer">1x Male GPIO Header</a>
- <a href="https://www.amazon.com/Teansic-Connector-Vertical-Charging-Product/dp/B09NKDQ1RL" target="_blank" rel="noopener noreferrer">3x Male and 3x Female USB Type A breakouts like the ones seen in this kit</a>
- <a href="https://www.adafruit.com/product/805" target="_blank" rel="noopener noreferrer">1x SPST or SPDT switch</a>
- <a href="https://www.aliexpress.us/item/3256801995101691.html" target="_blank" rel="noopener noreferrer">1x Fan</a>
- <a href="https://www.aliexpress.us/item/2255799828239708.html" target="_blank" rel="noopener noreferrer">2x A1 Ribbon FPV Connector and 1x FFC Ribbon Cable 5cm</a>
- <a href="https://raw.githubusercontent.com/fe-moldark/wesleykent-website/gh-pages/assets/circuit_diagram/DPDT_switch.png" target="_blank" rel="noopener noreferrer">1x 3-Pos 6 pin DPDT switch that looks something like this</a>
- 1x USB joystick (<a href="https://www.amazon.com/Rii-GP100-Controller-Raspberry-Windows/dp/B073Z9MKKH" target="_blank" rel="noopener noreferrer">this one should work</a>, I got mine in 2018 so it's no longer available), and you'll need to rip the guts out of this thing
- <a href="https://www.aliexpress.us/item/3256803023093138.html" target="_blank" rel="noopener noreferrer">1x 90 degree USB-C right angle adapter (option 5)</a>
- Wire ranging from 30 AWG for the buttons / LEDs, to 22 AWG for the speakers and some common power lines, to 16 gauge wire for the 5V 3A lines between the UPS and Pi board
- Solder, soldering iron, heat shrink tubing, perfboards / breadboards, wire cutters, etc.
- 2x plastic gears, 3x springs and superglue (reference video for more on this)
<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
