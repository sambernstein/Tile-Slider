# Tile-Slider
This is a group-theoretical puzzle game: a 2D grid of colored tiles with slidable rows and columns that wrap around. Rearrange the tiles so that each rectangular section of the grid has only tiles of its color.

### How to run

Run in Python 2.7 with the package `pygame` version `1.9.6` installed.

#### Original game
Run `python2 Slider.py` to play the original game. Click and drag the rows and columns to rearrange the tiles. Press keys `s` and `d` to switch between different boards.

#### AI Heuristic Version
Run `python2 AI_Slider.py`. You can click and drag rows and use `s` and `d` to switch between different boards. Press `a` to scramble the board, `0` to start or stop the AI solver, `l` to toggle between animating and not animating the AI solver, and `p` to pause and unpause. The AI solver uses a basic connectedness heuristic.
