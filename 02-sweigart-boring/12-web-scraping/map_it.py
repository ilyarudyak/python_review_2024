#! venv/bin/python
# map_it.py - Launches a map in the browser using an address from the
# command line or clipboard.

import webbrowser, sys, pyperclip

def open_map():
    """
    Open a map in the browser using an address from the command line or clipboard.
    """
    if len(sys.argv) > 1:
        # Get address from command line.
        address = ' '.join(sys.argv[1:])
    else:
        # Get address from clipboard.
        address = pyperclip.paste()

    print('Opening map in the browser for the address:', address)
    webbrowser.open('https://www.google.com/maps/place/' + address)

if __name__ == '__main__':
    open_map()