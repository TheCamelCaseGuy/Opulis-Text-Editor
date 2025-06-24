import curses
import threading
import time
import os
from datetime import datetime
import json
from pygments import lex
from pygments.lexers import TextLexer
from pygments.token import Token
from pygments.lexers.python import PythonLexer
from pygments.lexers.c_cpp import CppLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.html import HtmlLexer
from pygments.lexers.css import CssLexer
from pygments.lexers.ruby import RubyLexer
from pygments.lexers.json5 import Json5Lexer
from pygments.lexers.jvm import JavaLexer
from pygments.lexers.go import GoLexer
from pygments.lexers.rust import RustLexer
from colorama import Fore
import pyfiglet
import shutil
import subprocess
import urllib.request

def launchOpulisRepair():
    # Delete config.json if it exists
    confPath = os.path.join(os.getcwd(), "config.json")
    if os.path.exists(confPath):
        try:
            os.remove(confPath)
            print("config.json deleted successfully.")
            
        except Exception as e:
            print(f"Failed to delete config.json: {e}")
    # Define download URL and local save path
    repairUrl = "https://raw.githubusercontent.com/TheCamelCaseGuy/Opulis-Text-Editor/main/installer/repair.bat"
    localPath = os.path.join(os.environ.get("TEMP", "/tmp"), "repair_opulis.bat")
    
    try:
        # Download the repair.bat file
        print("Downloading repair script...")
        urllib.request.urlretrieve(repairUrl, localPath)

        # Execute the downloaded script
        print("Executing repair script...")
        subprocess.run([localPath], check=True, shell=True)
        print("Repair script completed successfully.")
    except Exception as e:
        print(f"Reinstallation Failed: {e}")
        



start = True

if os.path.exists("dev"):
    DEVELOPMENTMODE = True
else:
    DEVELOPMENTMODE = False

def log(message: str, level: str = "info", warnInError: bool = True):
    if DEVELOPMENTMODE:
        try:
            """Append a message to the log file with timestamp."""
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("editor.log", "a") as logfile:
                logfile.write(f"[{timestamp}] [{level.upper()}] {message}\n")
        except:
            log("Log skipped for an item.", "warn", False)

    elif level == "error":
        try:
            """Append a message to the log file with timestamp."""
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("errors.log", "a") as logfile:
                logfile.write(f"[{timestamp}] [{level.upper()}] {message}\n")
        except:
            log("Log skipped for an item.", "warn", False)

    elif level == "warn" and warnInError:
        try:
            """Append a message to the log file with timestamp."""
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("errors.log", "a") as logfile:
                logfile.write(f"[{timestamp}] [{level.upper()}] {message}\n")
        except:
            log("Log skipped for an item.", "warn", False)

log("Application startup initiated.", "info")

if True:
        SYNTAXTHEMES = {
            "stheno": {
                "keyword": (curses.COLOR_CYAN, curses.COLOR_BLACK),
                "string": (curses.COLOR_BLUE, curses.COLOR_BLACK),
                "comment": (curses.COLOR_GREEN, curses.COLOR_BLACK),
                "number": (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
                "function": (curses.COLOR_YELLOW, curses.COLOR_BLACK),
                "class": (curses.COLOR_RED, curses.COLOR_BLACK),
                "variable": (curses.COLOR_WHITE, curses.COLOR_BLACK),
                "operator": (curses.COLOR_CYAN, curses.COLOR_BLACK),
                "builtin": (curses.COLOR_YELLOW, curses.COLOR_BLACK)
            },
            "medusa": {
                "keyword": (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
                "string": (curses.COLOR_YELLOW, curses.COLOR_BLACK),
                "comment": (curses.COLOR_GREEN, curses.COLOR_BLACK),
                "number": (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
                "function": (curses.COLOR_GREEN, curses.COLOR_BLACK),
                "class": (curses.COLOR_CYAN, curses.COLOR_BLACK),
                "variable": (curses.COLOR_WHITE, curses.COLOR_BLACK),
                "operator": (curses.COLOR_RED, curses.COLOR_BLACK),
                "builtin": (curses.COLOR_BLUE, curses.COLOR_BLACK)
            },
            "euryale": {
                "keyword": (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
                "string": (curses.COLOR_YELLOW, curses.COLOR_BLACK),
                "comment": (curses.COLOR_BLUE, curses.COLOR_BLACK),
                "number": (curses.COLOR_CYAN, curses.COLOR_BLACK),
                "function": (curses.COLOR_GREEN, curses.COLOR_BLACK),
                "class": (curses.COLOR_RED, curses.COLOR_BLACK),
                "variable": (curses.COLOR_WHITE, curses.COLOR_BLACK),
                "operator": (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
                "builtin": (curses.COLOR_CYAN, curses.COLOR_BLACK)
            }
        }

SYNTAXTHEMENAMES = ["stheno", "medusa", "euryale"]


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
                "wordwrap": False,
                "syntaxTheme": "medusa",

            },

            "hotkeys": {
                "tabSize": 4,
                "indentWithTabs": True,

            },
            "intro": True,
            "creditScreen": True,
            "pluginsEnabled": True, # For future use
        }

        self.load()

    def load(self):
        log("Configuration file successfully loaded.", "info")
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                self.config = json.load(file)

    def save(self):
        log("Configuration file saved.", "info")
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
        log(f"Updated Configuration key '{path}' to '{str(value)}'", "debug")

    def get(self, path):
        keys = path.split(".")
        config = self.config
        for key in keys:
            if key not in config:
                return None
            config = config[key]
        log(f"Accessed configuration key '{path}' with value '{config}'.", "debug")
        return config

config = Config()


def getTime():
    """Returns the current datetime in a nicely formatted string."""
    return datetime.now().strftime("%I:%M %p")

def getDate():
    """Returns the current date in a nicely formatted string."""
    return datetime.now().strftime("%Y-%m-%d")

text = [""]
if config.get("autosave.enabled"):
    os.makedirs(config.get("autosave.path"), exist_ok=True)

    log(f"Creating directory '{config.get("autosave.path")}' if it does not exist.", "debug")
    path = os.path.join(config.get("autosave.path"), "autosave.txt")
    log("Determining autosave file path.", "info")

def autosave():
    while config.get("autosave.enabled"):
        TXT = "\n".join(text)
        if TXT:
            with open(path, "w") as file:
                file.write(TXT)
                log("Autosave completed successfully.")
        
        if len(TXT) < config.get("autosave.largeConsideration"):
            log("File size classified as 'small'", "debug")
            log(f"Autosave thread sleeping for {config.get("autosave.intervalSmall")} seconds.", "debug")
            time.sleep(config.get("autosave.intervalSmall"))
        else:
            log("File size classified as 'large'")
            time.sleep(config.get("autosave.intervalLarge"))
            log(f"Autosave thread sleeping for {config.get("autosave.intervalLarge")} seconds.", "debug")
        

if config.get("autosave.enabled"):
    log("Autosave is enabled.", "info")
    threading.Thread(target=autosave, daemon=True).start()

    log("Autosave thread initialized.", "info")

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

frameCount = 1

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
        log("Application started.", "info")
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
        log(f"set 'FILENAME' flag to 'False', 'SAVED' flag to 'False'.", "info")
        self.theme = config.get("appearance.theme")  # Default theme
        log("Fetched theme.", "info")
        self.initColors()

    def initColors(self):
        log("Initialized color palette.", "info")
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
        global frameCount
        log(f"Draw new frame ({frameCount} drawn).", "info")
        frameCount += 1

        # Get current syntax theme colors
        syntaxTheme = config.get("appearance.syntaxTheme")
        themeColors = SYNTAXTHEMES.get(syntaxTheme, SYNTAXTHEMES["medusa"])
        
        # Initialize color pairs for syntax highlighting
        for i, (key, (fg, bg)) in enumerate(themeColors.items(), start=20):
            curses.init_pair(i, fg, bg)

        TOKENCOLORS = {
            Token.Keyword: curses.color_pair(20),
            Token.Keyword.Constant: curses.color_pair(20),
            Token.Keyword.Declaration: curses.color_pair(20),
            Token.Literal.String: curses.color_pair(21),
            Token.Literal.String.Doc: curses.color_pair(21),
            Token.Literal.String.Single: curses.color_pair(21),
            Token.Literal.String.Double: curses.color_pair(21),
            Token.Comment.Single: curses.color_pair(22),
            Token.Comment.Multiline: curses.color_pair(22),
            Token.Literal.Number: curses.color_pair(23),
            Token.Name.Function: curses.color_pair(24),
            Token.Name.Class: curses.color_pair(25),
            Token.Name.Variable: curses.color_pair(26),
            Token.Name.Builtin: curses.color_pair(28),
            Token.Operator: curses.color_pair(27),
            Token.Name.Builtin.Pseudo: curses.color_pair(28),
            Token.Name.Variable.Instance: curses.color_pair(26),
            Token.Name.Variable.Class: curses.color_pair(26)
        }

        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        visibleLines = max_y - 2
        textAreaWidth = max_x - 6

        # Determine visible text range
        startLine = self.scrollOffset
        endLine = min(startLine + visibleLines, len(self.text))
        visibleText = self.text[startLine:endLine]

        # Select appropriate lexer
        if self.filename.endswith('.py'):
            lexer = PythonLexer()
        elif self.filename.endswith(('.cpp', '.c')):
            lexer = CppLexer()
        elif self.filename.endswith('.js'):
            lexer = JavascriptLexer()
        elif self.filename.endswith('.html'):
            lexer = HtmlLexer()
        elif self.filename.endswith('.css'):
            lexer = CssLexer()
        elif self.filename.endswith('.rb'):
            lexer = RubyLexer()
        elif self.filename.endswith('.json'):
            lexer = Json5Lexer()
        elif self.filename.endswith('.java'):
            lexer = JavaLexer()
        elif self.filename.endswith('.go'):
            lexer = GoLexer()
        elif self.filename.endswith('.rs'):
            lexer = RustLexer()
        else:
            lexer = TextLexer()

        displayY = 0
        wrappedLineCount = 0

        # Only process visible lines
        for i, line in enumerate(visibleText):
            lineIndex = startLine + i
            self.stdscr.addstr(displayY, 0, f"{lineIndex + 1:>3} ", curses.color_pair(1))
            self.stdscr.addstr(displayY, 4, config.get("appearance.marginChar") + " ")

            if config.get("appearance.wordwrap"):
                remaining = line
                while remaining and displayY < visibleLines:
                    if len(remaining) <= textAreaWidth:
                        segment = remaining
                        remaining = ""
                    else:
                        wrapPoint = textAreaWidth
                        if ' ' in remaining[:textAreaWidth]:
                            wrapPoint = remaining[:textAreaWidth].rindex(' ')
                        segment = remaining[:wrapPoint]
                        remaining = remaining[wrapPoint:].lstrip()

                    pos = 6
                    try:
                        for token, text in lex(segment, lexer):
                            color = TOKENCOLORS.get(token, curses.color_pair(0))
                            self.stdscr.addstr(displayY, pos, text, color)
                            pos += len(text)
                    except:
                        self.stdscr.addstr(displayY, 6, segment)

                    if remaining:
                        displayY += 1
                        wrappedLineCount += 1
                        if displayY >= visibleLines:
                            break
                        self.stdscr.addstr(displayY, 0, "   ", curses.color_pair(1))
                        self.stdscr.addstr(displayY, 4, config.get("appearance.marginChar") + " ")
            else:
                visibleSegment = line[self.horizontalOffset:self.horizontalOffset + textAreaWidth]
                pos = 6
                try:
                    for token, text in lex(visibleSegment, lexer):
                        color = TOKENCOLORS.get(token, curses.color_pair(0))
                        self.stdscr.addstr(displayY, pos, text, color)
                        pos += len(text)
                except:
                    self.stdscr.addstr(displayY, 6, visibleSegment)

            displayY += 1

        # Status bar updates
        charCount = sum(len(line) for line in self.text)
        if self.FLAGS["FILENAME"]:
            try:
                with open(self.filename, "r") as file:
                    data = file.read()
                    self.FLAGS["SAVED"] = (data == "\n".join(self.text))
            except:
                self.FLAGS["SAVED"] = False

        saveChar = "*" if not self.FLAGS["SAVED"] else ""
        wrapStatus = "Wrap BETA" if config.get("appearance.wordwrap") else "No Wrap"
        statusText = f" {getTime()} | {saveChar}{self.filename} | Ln {self.cursorY+1}, Col {self.cursorX+1} | {wrapStatus} | Chars: {charCount} | Theme: {self.theme} | Syntax: {syntaxTheme} | ESC to exit"
        self.stdscr.addstr(max_y - 1, 0, statusText[:max_x-1].ljust(max_x-1), curses.color_pair(2) | curses.A_BOLD)

        cursorY = self.cursorY - self.scrollOffset + wrappedLineCount
        cursorX = self.cursorX - self.horizontalOffset + 6
        if 0 <= cursorY < max_y - 1 and 0 <= cursorX < max_x:
            self.stdscr.move(cursorY, cursorX)

        self.stdscr.refresh()

    def run(self):
        while start:
            self.displayEditor()
            key = self.stdscr.getch()
            max_y, max_x = self.stdscr.getmaxyx()
            visible_lines = max_y - 2
            text_area_width = max_x - 6

            global text
            text = self.text
            log(f"Keypress received: code={str(key)} (character='{chr(key)}').", "info")
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
                log("ESC pressed, exiting text editor.", "debug")
                break

            elif key == 19:  # Ctrl+S
                log("Attempting to save file.", "info")
                if self.FLAGS["FILENAME"]:
                    log("Filename already provided for saving file.", "info")
                    self.saveFile(self.filename)
                else:
                    log("No filename provided. Prompting user for filename.", "info")
                    filename = self.getFilename("Save as: ")
                    if filename:
                        self.saveFile(filename)
                        self.FLAGS["FILENAME"] = True
                        log("set 'FILENAME' flag to 'True'.", "info")
                        self.filename = filename
                    else:
                        log("No filename provided for saving file.", "warn")


            elif key == 15:  # Ctrl+O
                filename = self.getFilename("Open file: ")
                if filename:
                    self.loadFile(filename)
                    self.FLAGS["FILENAME"] = True
                    log("set 'FILENAME' flag to 'True'.", "info")
                    self.filename = filename
                    log("Undo stack cleared", "debug")
                    self.undoStack = []
                    log(f"File {filename} opened successfully.")
                else:
                    log("No filename provided for opening file.", "warn")

            elif key == 26 and self.undoStack:  # Ctrl+Z
                log("Undo operation executed.", "info")
                self.text = self.undoStack.pop()

            elif key == 20:  # Ctrl+T
                self.switchTheme()
                log(f"THEME loaded: {config.get("appearance.theme")}", "info")
                

            elif key >= 32 and key <= 126:
                log(f"Inserted character '{chr(key)}' at cursor position", "info")
                self.undoStack.append([row[:] for row in self.text])
                self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX] +
                                           chr(key) + self.text[self.cursorY][self.cursorX:])
                self.cursorX += 1
                if self.cursorX >= self.horizontalOffset + text_area_width:
                    self.horizontalOffset += 1

            elif key == 4:  # Ctrl+D
                print("Deleted current line.", "info")
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
                    log("Indentation is enabled, executed instruction.", "info")
                    self.undoStack.append([row[:] for row in self.text])
                    self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX] +
                                            " " * config.get("hotkeys.tabSize") + self.text[self.cursorY][self.cursorX:])
                    self.cursorX += 4
                    if self.cursorX >= self.horizontalOffset + text_area_width:
                        self.horizontalOffset += 1

            elif key == 23:  # Ctrl+W
                config.update("appearance.wordwrap", not config.get("appearance.wordwrap"))
                log(f"Word Wrap status set to '{config.get("appearance.wordwrap")}'")

            elif key == curses.KEY_DC:  # Delete key
                log("CHAR DELETED")
                if self.cursorX < len(self.text[self.cursorY]):
                    self.undoStack.append([row[:] for row in self.text])
                    self.text[self.cursorY] = (self.text[self.cursorY][:self.cursorX] + 
                                              self.text[self.cursorY][self.cursorX + 1:])
                elif self.cursorY < len(self.text) - 1:
                    self.undoStack.append([row[:] for row in self.text])
                    self.text[self.cursorY] += self.text.pop(self.cursorY + 1)

            elif key == 14:  # Ctrl+N
                log("File cleared.", "info")
                self.cursorX, self.cursorY = 0, 0
                self.scrollOffset = 0
                self.horizontalOffset = 0
                self.text = [""]
                self.undoStack = []
                self.FLAGS["FILENAME"] = False
                self.filename = "Untitled"
                self.FLAGS["SAVED"] = True

            elif key == 18:  # Ctrl+R
                themes = SYNTAXTHEMENAMES
                currentTheme = config.get("appearance.syntaxTheme")
                currentIndex = themes.index(currentTheme)
                nextTheme = themes[(currentIndex + 1) % len(themes)]
                config.update("appearance.syntaxTheme", nextTheme)
                log(f"S_THEME loaded: {nextTheme}", "info")

            elif key == 12:  # Ctrl+L
                log("Opening Settings menu.", "info")
                self.stdscr.clear()
                self.loadFile("config.json")
                self.FLAGS["FILENAME"] = True
                log("set 'FILENAME' flag to 'True'.", "info")
                self.filename = "config.json"
                log(f"File {self.filename} opened successfully.")


    def getFilename(self, prompt):
        log("User input method called.", "info")
        curses.echo()
        max_y, max_x = self.stdscr.getmaxyx()
        self.stdscr.addstr(max_y - 3, 0, prompt)
        self.stdscr.refresh()
        filename = self.stdscr.getstr(max_y - 2, 0, 50).decode("utf-8")
        curses.noecho()
        return filename.strip()

    def saveFile(self, filename):
        try:
            with open(filename, "w") as file:
                file.write("\n".join(self.text))

        except Exception as e:
            log(f"File {filename} failed to save! Error: {e}", "error")
        else:
            log(f"File {filename} saved successfully.", "info")

    def loadFile(self, filename):
        try:
            with open(filename, "r") as file:
                self.text = file.read().split("\n")
                self.cursorX, self.cursorY = 0, 0
                self.scrollOffset = 0
                self.horizontalOffset = 0
        except FileNotFoundError:
            log(f"File {filename} was not found!", "error")
            raise FileNotFoundError(f"File {filename} was not found!")
        except Exception as e:
            log(f"File {filename} failed to load! Error: {e}", "error")
        else:
            log(f"File '{filename}' loaded successfully.", "info")

def main(stdscr):
    editor = TextEditor(stdscr)
    editor.run()

terminalSize = shutil.get_terminal_size()
terminalWidth = terminalSize.columns
terminalHeight = terminalSize.lines


if config.get("creditScreen"):

    os.system('cls')

    asciiArt = pyfiglet.figlet_format("Opulis Text Editor", font="slant")


    # Center each line horizontally
    centeredArt = "\n".join([line.center(terminalWidth) for line in asciiArt.split("\n")])

    # Calculate vertical padding
    paddingLines = (terminalHeight - len(centeredArt.split("\n"))) // 2
    verticalPadding = "\n" * paddingLines

    # Print centered ASCII art
    print(Fore.LIGHTBLUE_EX + verticalPadding + centeredArt + verticalPadding + Fore.RESET)

    time.sleep(4)
    os.system('cls')

try:
    if config.get("intro"):
        log("Intro screen displayed.", "info")
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
        config.update("intro", False)
        curses.wrapper(main)

    else:
        curses.wrapper(main)
except Exception as e:
    log(f"An error occurred: {e}", "error")
    print(f"An error occurred: {e}")
    print("Write 'repair' to reset your installation or press enter to exit.")
    userInput = input()
    if userInput.lower() == "repair":
        os.system('cls')
        asciiArt = pyfiglet.figlet_format("Opulis Repair Tool", font="slant")


        # Center each line horizontally
        centeredArt = "\n".join([line.center(terminalWidth) for line in asciiArt.split("\n")])

        # Calculate vertical padding
        paddingLines = (terminalHeight - len(centeredArt.split("\n"))) // 2
        verticalPadding = "\n" * paddingLines

        # Print centered ASCII art
        print(Fore.LIGHTRED_EX + verticalPadding + centeredArt + verticalPadding + Fore.RESET)
        time.sleep(3)
        launchOpulisRepair()
        exit()
    else:
        os.system('cls')
        asciiArt = pyfiglet.figlet_format("ERROR", font="slant")


        # Center each line horizontally
        centeredArt = "\n".join([line.center(terminalWidth) for line in asciiArt.split("\n")])

        # Calculate vertical padding
        paddingLines = (terminalHeight - len(centeredArt.split("\n"))) // 2
        verticalPadding = "\n" * paddingLines

        # Print centered ASCII art
        print(Fore.LIGHTRED_EX + verticalPadding + centeredArt + verticalPadding + Fore.RESET)
        time.sleep(3)
        exit()