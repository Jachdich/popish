# Popysh - POpup PYthon SHell

Just a quick script to allow you to type out python expressions at the tap of a button.

## Installation

`main.py` is a single file executable script - put it wherever you normally put your scripts. Renaming is recommended.

### Dependencies

- PyQt5
- pyperclip (clipboard support)

Run `pip install -r requirements.txt` to automatically install.

## Usage

For best results, use your window manager or utility of choice to bind a key combination to run the script. When run, you can type in the text box and the result of the expression will be displayed below in real time. Only the result of the very last line is displayed. The previous lines are run as statements, so you can put variable assignments etc. on previous lines just like you would in a normal program. Currently, more complex constructs involving indented blocks are not supported, however this is being worked on.

## Configuration

At the top of the file is defined a list of constants. Add any constants you feel are useful (or, even better, open an issue or PR to suggest they're added by default!). The style can be changed using the QSS string found near the top of the program. TODO: add built-in and user-added themes.

## Keybinds

- Ctrl-C (no text selected) - copy result to the clipboard
- Ctrl-C (text selected) - copy selected text from the code to the clipboard
- Esc - Quit

## TODO

- [ ] Also save code to a file?
- [ ] Show autocomplete options?
- [ ] Add themes, built in and external
- [ ] Make multi-line programs properly work
- [ ] Figure out the weird bug with list comprehensions
- [ ] Syntax highlighting
