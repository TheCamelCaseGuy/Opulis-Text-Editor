import curses
import threading
import time
import os
from datetime import datetime
import json

class Config:
    def __init__(self):
        self.config = {
            "autosave": {
                "enabled": True,
                "intervalLarge": 10,
                "intervalSmall": 3,
                "path": "autosave/",
                "largeConsideration": 3000,

            },

            "appearance": {
                "theme": "ocean",
                "marginChar": "│",
                "wordwrap": True

            },

            "hotkeys": {
                "tabSize": 4,
                "indentWithTabs": True,

            },
            "intro": False,
            "pluginsEnabled": True # For future use
        }

        self.load()

    def load(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                self.config = json.load(file)

    def save(self):
        with open("config.json", "w") as file:
            json.dump(self.config, file, indent=4)

    def update(self, path, value):
        keys = path.split(".")
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save()

    def get(self, path):
        keys = path.split(".")
        config = self.config
        for key in keys:
            if key not in config:
                return None
            config = config[key]
        return config

config = Config()


def getTime():
    """Returns the current datetime in a nicely formatted string."""
    return datetime.now().strftime("%I:%M %p")

def getDate():
    """Returns the current date in a nicely formatted string."""
    return datetime.now().strftime("%Y-%m-%d")

text = [""]

os.makedirs(config.get("autosave.path"), exist_ok=True)
path = os.path.join(config.get("autosave.path"), "autosave.txt")

def autosave():
    while config.get("autosave.enabled"):
        TXT = "\n".join(text)
        if TXT:
            with open(path, "w") as file:
                file.write(TXT)
        
        if len(TXT) < config.get("autosave.largeConsideration"):
            time.sleep(config.get("autosave.intervalSmall"))
        else:
            time.sleep(config.get("autosave.intervalLarge"))

threading.Thread(target=autosave, daemon=True).start()

THEMES = {
    "ocean": (curses.COLOR_CYAN, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_BLUE),
    "dark": (curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK),
    "solarized": (curses.COLOR_YELLOW, curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_YELLOW),
    "blood": (curses.COLOR_RED, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_RED),
    "cherry": (curses.COLOR_MAGENTA, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_MAGENTA),
    "nature": (curses.COLOR_GREEN, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_GREEN),
    "radiant": (curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE),
    "bloom": (curses.COLOR_MAGENTA, curses.COLOR_CYAN, curses.COLOR_WHITE, curses.COLOR_GREEN),
    "vanilla": (curses.COLOR_WHITE, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK),
    
}

# copy a file to the current directory
def copyFile(filename, newfilename):
    currentdir = os.getcwd()
    if not os.path.exists(os.path.join(currentdir, filename)):
        with open(filename, "r") as file:
            data = file.read()
        with open(os.path.join(currentdir, newfilename), "w") as file:
            file.write(data)


class TextEditor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.text = [""]
        self.cursorX, self.cursorY = 0, 0
        self.scrollOffset = 0  # Tracks the topmost visible line
        self.horizontalOffset = 0  # Tracks the leftmost visible column
        self.undoStack = []
        self.filename = "Untitled"
        self.FLAGS = {
            "FILENAME": False,
            "SAVED": True
        }
        self.theme = config.get("appearance.theme")  # Default theme
        self.initColors()

    def initColors(self):
        curses.start_color()
        fg1, bg1, fg2, bg2 = THEMES[self.theme]
        curses.init_pair(1, fg1, bg1)  # Line number color
        curses.init_pair(2, fg2, bg2)  # Status bar color
        curses.curs_set(1)

    def switchTheme(self):
        themes = list(THEMES.keys())
        currentIndex = themes.index(self.theme)
        self.theme = themes[(currentIndex + 1) % len(themes)]  # Rotate to next theme
        config.update("appearance.theme", self.theme)  # Save the new theme to config
        self.initColors()

    def displayEditor(self):
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        visibleLines = max_y - 2
        textAreaWidth = max_x - 6

        displayY = 0
        wrappedLineCount = 0  # Track wrapped lines before cursor
        i = 0
        while i < visibleLines and self.scrollOffset + i < len(self.text):
            lineIndex = self.scrollOffset + i
            line = self.text[lineIndex]
            
            if config.get("appearance.wordwrap"):
                displayLines = []
                remaining = line
                while len(remaining) > textAreaWidth:
                    wrapPoint = textAreaWidth
                    if ' ' in remaining[:textAreaWidth]:
                        wrapPoint = remaining[:textAreaWidth].rindex(' ')
                    displayLines.append(remaining[:wrapPoint])
                    remaining = remaining[wrapPoint:].lstrip()
                displayLines.append(remaining)
                
                # Count wrapped lines before cursor position
                if lineIndex < self.cursorY:
                    wrappedLineCount += len(displayLines) - 1
                
                for j, segment in enumerate(displayLines):
                    if displayY >= visibleLines:
                        break
                    if j == 0:
                        self.stdscr.addstr(displayY, 0, f"{lineIndex + 1:>3} ", curses.color_pair(1))
                        self.stdscr.addstr(displayY, 4, (config.get("appearance.marginChar") + " "))
                        self.stdscr.addstr(displayY, 6, segment)
                    else:
                        self.stdscr.addstr(displayY, 0, "   ", curses.color_pair(1))
                        self.stdscr.addstr(displayY, 4, (config.get("appearance.marginChar") + " "))
                        self.stdscr.addstr(displayY, 6, segment)
                    displayY += 1
                i += 1
            else:
                self.stdscr.addstr(i, 0, f"{lineIndex + 1:>3} ", curses.color_pair(1))
                self.stdscr.addstr(i, 4, (config.get("appearance.marginChar") + " "))
                visible_text = line[self.horizontalOffset:self.horizontalOffset + textAreaWidth]
                self.stdscr.addstr(i, 6, visible_text)
                displayY += 1
                i += 1

        charCount = sum(len(line) for line in self.text)
        filenameDisplay = self.filename
        if self.FLAGS["FILENAME"]:
            with open(filenameDisplay, "r") as file:
                data = file.read()
                if data == "\n".join(self.text):
                    self.FLAGS["SAVED"] = True
                else:
                    self.FLAGS["SAVED"] = False

        saveChar = "*" if not self.FLAGS["SAVED"] else ""
        wrapStatus = "Wrap" if config.get("appearance.wordwrap") else "No Wrap"
        statusText = f" {getTime()} | {saveChar}{filenameDisplay} | Ln {self.cursorY+1}, Col {self.cursorX+1} | {wrapStatus} | Chars: {charCount} | Theme: {self.theme} | ESC to exit"
        trimmedStatus = statusText[:max_x - 1]
        self.stdscr.addstr(max_y - 1, 0, trimmedStatus.ljust(max_x - 1), curses.color_pair(2) | curses.A_BOLD)

        # Adjust cursor position with wrapped lines offset
        cursorVisibleY = self.cursorY - self.scrollOffset + wrappedLineCount
        cursorVisibleX = self.cursorX - self.horizontalOffset + 6
        if 0 <= cursorVisibleY < max_y - 1 and 0 <= cursorVisibleX < max_x:
            self.stdscr.move(cursorVisibleY, cursorVisibleX)
        self.stdscr.refresh()

    def run(self):
        while True:
            self.displayEditor()
            key = self.stdscr.getch()
            max_y, max_x = self.stdscr.getmaxyx()
            visible_lines = max_y - 2
            text_area_width = max_x - 6

            global text
            text = self.text

            if key == curses.KEY_UP:
                if self.cursorY > 0:
                    self.cursorY -= 1
                    self.cursorX = min(self.cursorX, len(self.text[self.cursorY]))
                if self.cursorY < self.scrollOffset:
                    self.scrollOffset -= 1

            elif key == curses.KEY_DOWN:
                if self.cursorY < len(self.text) - 1:
                    self.cursorY += 1
                    self.cursorX = min(self.cursorX, len(self.text[self.cursorY]))
                if self.cursorY >= self.scrollOffset + visible_lines:
                    self.scrollOffset += 1

            elif key == curses.KEY_LEFT and self.cursorX > 0:
                self.cursorX -= 1
                if self.cursorX < self.horizontalOffset:
                    self.horizontalOffset = max(0, self.horizontalOffset - 1)

            elif key == curses.KEY_RIGHT:
                if self.cursorX < len(self.text[self.cursorY]):
                    self.cursorX += 1
                    if self.cursorX >= self.horizontalOffset + text_area_width:
                        self.horizontalOffset += 1

            elif key == ord('\n'):
                self.undoStack.append([row[:] for row in self.text])
                self.text.insert(self.cursorY + 1, self.text[self.cursorY][self.cursorX:])
                self.text[self.cursorY] = self.text[self.cursorY][:self.cursorX]
                self.cursorY += 1
                self.cursorX = 0
                self.horizontalOffset = 0
                if self.cursorY >= self.scrollOffset + visible_lines:
                    self.scrollOffset += 1

            elif key == ord('\b') or key == 127:
                if self.cursorX > 0:
                    self.undoStack.append([row[:] for row in self.text])
                    self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX - 1] +
                                               self.text[self.cursorY][self.cursorX:])
                    self.cursorX -= 1
                    if self.cursorX < self.horizontalOffset:
                        self.horizontalOffset = max(0, self.horizontalOffset - 1)
                elif self.cursorY > 0:
                    self.undoStack.append([row[:] for row in self.text])
                    prev_line = self.text.pop(self.cursorY)
                    self.cursorY -= 1
                    self.cursorX = len(self.text[self.cursorY])
                    self.text[self.cursorY] += prev_line
                    if self.cursorY < self.scrollOffset:
                        self.scrollOffset -= 1

            elif key == 27:
                break

            elif key == 19:  # Ctrl+S
                if self.FLAGS["FILENAME"]:
                    self.saveFile(self.filename)
                else:
                    filename = self.getFilename("Save as: ")
                    if filename:
                        self.saveFile(filename)
                        self.FLAGS["FILENAME"] = True
                        self.filename = filename

            elif key == 15:  # Ctrl+O
                filename = self.getFilename("Open file: ")
                if filename:
                    self.loadFile(filename)
                    self.FLAGS["FILENAME"] = True
                    self.filename = filename
                    self.undoStack = []

            elif key == 26 and self.undoStack:  # Ctrl+Z
                self.text = self.undoStack.pop()

            elif key == 20:  # Ctrl+T
                self.switchTheme()

            elif key >= 32 and key <= 126:
                self.undoStack.append([row[:] for row in self.text])
                self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX] +
                                           chr(key) + self.text[self.cursorY][self.cursorX:])
                self.cursorX += 1
                if self.cursorX >= self.horizontalOffset + text_area_width:
                    self.horizontalOffset += 1

            elif key == 4:  # Ctrl+D
                if self.cursorY < len(self.text):
                    self.undoStack.append([row[:] for row in self.text])
                    self.text.pop(self.cursorY)
                    if not self.text:
                        self.text = [""]
                    if self.cursorY >= len(self.text):
                        self.cursorY = len(self.text) - 1
                    self.cursorX = min(self.cursorX, len(self.text[self.cursorY]))
                    self.horizontalOffset = 0
                    self.stdscr.clear()

            elif key == 9:  # Tab key
                if config.get("hotkeys.indentWithTabs"):
                    self.undoStack.append([row[:] for row in self.text])
                    self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX] +
                                            " " * config.get("hotkeys.tabSize") + self.text[self.cursorY][self.cursorX:])
                    self.cursorX += 4
                    if self.cursorX >= self.horizontalOffset + text_area_width:
                        self.horizontalOffset += 1

            elif key == 23:  # Ctrl+W
                config.update("appearance.wordwrap", not config.get("appearance.wordwrap"))

            elif key == curses.KEY_DC:  # Delete key
                if self.cursorX < len(self.text[self.cursorY]):
                    self.undoStack.append([row[:] for row in self.text])
                    self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX] + 
                                              self.text[self.cursorY][self.cursorX + 1:])
                elif self.cursorY < len(self.text) - 1:
                    self.undoStack.append([row[:] for row in self.text])
                    self.text[self.cursorY] += self.text.pop(self.cursorY + 1)

            elif key == 18:  # Ctrl+R
                self.cursorX, self.cursorY = 0, 0
                self.scrollOffset = 0
                self.horizontalOffset = 0
                self.text = [""]
                self.undoStack = []
                self.FLAGS["FILENAME"] = False
                self.filename = "Untitled"
                self.FLAGS["SAVED"] = True

            
            
            
            
                

    def getFilename(self, prompt):
        curses.echo()
        max_y, max_x = self.stdscr.getmaxyx()
        self.stdscr.addstr(max_y - 3, 0, prompt)
        self.stdscr.refresh()
        filename = self.stdscr.getstr(max_y - 2, 0, 50).decode("utf-8")
        curses.noecho()
        return filename.strip()

    def saveFile(self, filename):
        with open(filename, "w") as file:
            file.write("\n".join(self.text))

    def loadFile(self, filename):
        try:
            with open(filename, "r") as file:
                self.text = file.read().split("\n")
                self.cursorX, self.cursorY = 0, 0
                self.scrollOffset = 0
                self.horizontalOffset = 0
        except FileNotFoundError:
            pass

def main(stdscr):
    editor = TextEditor(stdscr)
    editor.run()


if not config.get("intro"):
    print("Welcome to Opulis Text Editor")
    print()
    print("Opulis is a minimal, open-source text editor.")
    input("Press Enter to continue...")
    print("Hotkeys:")
    print("Ctrl+S : Save file")
    print("Ctrl+O : Open file")
    print("Ctrl+Z : Undo")
    print("Ctrl+T : Switch theme")
    print("Ctrl+D : Delete current line")
    print("Ctrl+W : Toggle word wrap")
    print("Ctrl+R : Reset editor")
    print("Tab   : Insert indentation")
    print("Arrow keys : Navigate text")
    print("Delete : Remove character after cursor")
    print("Backspace : Remove character before cursor")
    print("ESC : Exit editor")
    print()
    input("Press Enter to continue...")
    config.update("intro", True)
    curses.wrapper(main)

else:
    curses.wrapper(main)
