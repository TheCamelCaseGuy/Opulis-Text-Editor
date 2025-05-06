import curses
import threading
import time
import os
from datetime import datetime

def getTime():
    """Returns the current datetime in a nicely formatted string."""
    return datetime.now().strftime("%I:%M %p")

def getDate():
    """Returns the current date in a nicely formatted string."""
    return datetime.now().strftime("%Y-%m-%d")

# Example usage
print(getTime())

text = [""]

os.makedirs("autosave", exist_ok=True)
path = os.path.join("autosave", "autosave.txt")

def autosave():
    while True:
        with open(path, "w") as file:
            file.write("\n".join(text))
        time.sleep(10)  # Autosave every 10 seconds

threading.Thread(target=autosave, daemon=True).start()

THEMES = {
    "ocean": (curses.COLOR_CYAN, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_BLUE),
    "dark": (curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK),
    "solarized": (curses.COLOR_YELLOW, curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_YELLOW),
    "blood": (curses.COLOR_RED, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_RED),
    "cherry": (curses.COLOR_MAGENTA, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_MAGENTA),
    "nature": (curses.COLOR_GREEN, curses.COLOR_BLACK, curses.COLOR_WHITE, curses.COLOR_GREEN),
}

class TextEditor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.text = [""]
        self.cursorX, self.cursorY = 0, 0
        self.scrollOffset = 0  # Tracks the topmost visible line
        self.undoStack = []
        self.filename = "Untitled"
        self.FLAGS = {
            "FILENAME": False,
            "SAVED": True
        }
        self.theme = "ocean"  # Default theme
        self.initColors()

    def initColors(self):
        curses.start_color()
        fg1, bg1, fg2, bg2 = THEMES[self.theme]
        curses.init_pair(1, fg1, bg1)  # Line number color
        curses.init_pair(2, fg2, bg2)  # Status bar color
        curses.curs_set(1)

    def switchTheme(self):
        themes = list(THEMES.keys())
        current_index = themes.index(self.theme)
        self.theme = themes[(current_index + 1) % len(themes)]  # Rotate to next theme
        self.initColors()

    def displayEditor(self):
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()  # Get screen size
        visible_lines = max_y - 2  # Leave space for the status bar

        for i in range(visible_lines):
            line_index = self.scrollOffset + i
            if line_index >= len(self.text):
                break
            line = self.text[line_index]
            self.stdscr.addstr(i, 0, f"{line_index + 1:>3} ", curses.color_pair(1))  # Line number
            self.stdscr.addstr(i, 4, "│ ")  # Separator line
            self.stdscr.addstr(i, 6, line[:max_x - 6])  # Actual text

        # Enhanced status bar with more info
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
        statusText = f" {getTime()} | {saveChar}{filenameDisplay} | Ln {self.cursorY+1}, Col {self.cursorX+1} | Chars: {charCount} | Theme: {self.theme}  | ESC to exit"
        trimmedStatus = statusText[:max_x - 1]  # Ensure it fits within screen width
        self.stdscr.addstr(max_y - 1, 0, trimmedStatus.ljust(max_x - 1), curses.color_pair(2) | curses.A_BOLD)

        # Adjust cursor position relative to the visible portion
        cursor_visible_y = self.cursorY - self.scrollOffset
        self.stdscr.move(cursor_visible_y, self.cursorX + 6)
        self.stdscr.refresh()

    def run(self):
        while True:
            self.displayEditor()
            key = self.stdscr.getch()
            max_y, _ = self.stdscr.getmaxyx()
            visible_lines = max_y - 2  # Leave space for the status bar

            global text
            text = self.text

            if key == curses.KEY_UP:

                if self.cursorY > 0:
                    self.cursorY -= 1

                if self.cursorY < self.scrollOffset:
                    self.scrollOffset -= 1

            elif key == curses.KEY_DOWN:

                if self.cursorY < len(self.text) - 1:
                    self.cursorY += 1

                if self.cursorY >= self.scrollOffset + visible_lines:
                    self.scrollOffset += 1

            elif key == curses.KEY_LEFT and self.cursorX > 0:
                self.cursorX -= 1

            elif key == curses.KEY_RIGHT and self.cursorX < len(self.text[self.cursorY]):
                self.cursorX += 1

            elif key == ord('\n'):
                self.undoStack.append([row[:] for row in self.text])
                self.text.insert(self.cursorY + 1, "")
                self.cursorY += 1
                self.cursorX = 0

                if self.cursorY >= self.scrollOffset + visible_lines:
                    self.scrollOffset += 1

            elif key == ord('\b') or key == 127:

                if self.cursorX > 0:
                    self.undoStack.append([row[:] for row in self.text])
                    self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX - 1] +
                                               self.text[self.cursorY][self.cursorX:])
                    
                    self.cursorX -= 1

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

            elif key == 19:  # Ctrl+S (Save)

                if self.FLAGS["FILENAME"]:
                    self.saveFile(self.filename)

                else:
                    filename = self.getFilename("Save as: ")

                    if filename:
                        self.saveFile(filename)
                        self.FLAGS["FILENAME"] = True
                        self.filename = filename

            elif key == 15:  # Ctrl+O (Open)

                filename = self.getFilename("Open file: ")

                if filename:
                    self.loadFile(filename)
                    self.FLAGS["FILENAME"] = True
                    self.filename = filename

            elif key == 26 and self.undoStack:  # Ctrl+Z (Undo)
                self.text = self.undoStack.pop()

            elif key == 20:  # Ctrl+T (Switch theme)
                self.switchTheme()
                
            elif key >= 32 and key <= 126:
                self.undoStack.append([row[:] for row in self.text])
                self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX] +
                                           chr(key) + self.text[self.cursorY][self.cursorX:])
                self.cursorX += 1

    def getFilename(self, prompt):
        curses.echo()
        max_y, max_x = self.stdscr.getmaxyx()
        self.stdscr.addstr(max_y - 3, 0, prompt)  # Move prompt one line higher
        self.stdscr.refresh()
        filename = self.stdscr.getstr(max_y - 2, 0, 50).decode("utf-8")  # User input one line above the last
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
        except FileNotFoundError:
            pass

def main(stdscr):
    editor = TextEditor(stdscr)
    editor.run()

curses.wrapper(main)
