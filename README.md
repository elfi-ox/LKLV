# LKLV

There are 2 apps in these repositories
 - [app/LKLV.pyw](https://github.com/elfi-ox/LKLV/blob/main/app/LKLV.pyw) is the Keybord Layout Vizualizer, When the file is executed it will launch [app/hotkeymonitor.ahk](https://github.com/elfi-ox/LKLV/blob/main/app/hotkeymonitor.ahk). This file needs [AutoHotKey](https://www.autohotkey.com) to run and is needed to communicate the key presses to the app API. The Fn key is not detectable by the OS, you will see in the AutoHotKey file that it is set to return 0. If you want to use that key, you will need to configure this script and your keyboard to communicate when the Fn key is being pressed.
<br>ㅤㅤㅤ 
<br>`Ctrl` `+` : Increase the app size
<br>`Ctrl` `-` : Decrease the app size
<br>`Ctrl` `M` : Mask the TitleBar (while masked, using `Alt`+`Tab` will bring the app to the front if it gets masked by another window)
<br>ㅤㅤㅤ 
<br>ㅤㅤㅤYou can compile [app/LKLV.pyw](https://github.com/elfi-ox/LKLV/blob/main/app/LKLV.pyw) into an executable with tools like [Auto PY to EXE](https://pypi.org/project/auto-py-to-exe/) if you wish to have a proper icon like [this one](https://github.com/elfi-ox/LKLV/blob/main/app/icon.ico) in your taskbar instead of the python window logo.

- [LayerMaker/xlsx to png.py](https://github.com/elfi-ox/LKLV/blob/main/LayerMaker/xlsx%20to%20png.py) is the app that will generate, when executed, the keyboard template used by LKLV.pyw in the [app/Layers](https://github.com/elfi-ox/LKLV/tree/main/app/Layers) folder, it will do so based on the [LayerMaker/KeybordLayout.xlsx](https://github.com/elfi-ox/LKLV/blob/main/LayerMaker/KeybordLayout.xlsx) spreadsheet. It is ***HEAVILY*** recommended to run this file with Excel to modify the keys because it relies on conditonal formating and checkboxes.

In this configuration, this app is configured to display a customized Optimot Layout on a keyboard with the shape of the [Keychron V5 Max ISO](https://www.keychron.com/products/keychron-v5-max-qmk-via-wireless-custom-mechanical-keyboard-iso-layout-collection?variant=41125308530777). The keys are easily editable in the Excel spreedsheet but changing the shape of the keyboard will require heavy changes to [LayerMaker/KeybordLayout.xlsx](https://github.com/elfi-ox/LKLV/blob/main/LayerMaker/KeybordLayout.xlsx) and [LayerMaker/xlsx to png.py](https://github.com/elfi-ox/LKLV/blob/main/LayerMaker/xlsx%20to%20png.py). I'm not willing to do more developpement of this app to support other keybord or layout or to implement ways of making it easier, as it is a personal project to begin with. But if you have any question for making you own version, don't hesitate to contact me, I will gladely help !
