# Opulis Text Editor
Opulis is a minimal, open-source text editor that can run in the windows terminal.

#
# The TUI System

The Opulis Editor offers a TUI, this results in a lower impact on the computer's performance. it can be fully controlled by the keyboard without a mouse.

#
# Hotkeys

| Hotkey  | Action |
| ------------- | ------------- |
| Ctrl+S  | Save File  |
| Ctrl+O  | Open File  |
| Ctrl+Z  | Undo |
| Ctrl+T  | Change Theme |
| Ctrl+N | New Draft |
| Ctrl+D | Delete Line |
| Ctrl+R | Change Syntax Theme |
| Ctrl+W | Toggle Word Wrap |
| Ctrl+L | Open Settings File |
| Tab | Indentation |

Yes, they are limited, but i plan to add a lot more in future releases

#
# Configuration
| Path  | Action |
| ------------- | ------------- |
| appearance.theme  | Changes The Theme Of The Editor |
| appearance.marginChar  | Character That Separates Numbers From Text |
| appearance.wordwrap  | Enables Word Wrap |
| appearance.syntaxTheme | Changes The Syntax Theme Of The Editor |
| autosave.enabled  | Enables Autosave |
| autosave.intervalLarge  | Autosave Cooldown For Large Files |
| autosave.intervalSmall  | Autosave Cooldown For Small Files |
| autosave.path  | Changes Autosave File Path  |
| autosave.largeConsideration  | Number Of Characters Required In A File For It To Be Considered Large |
| hotkeys.tabSize  | Size Of Tab Key Indentation |
| hotkeys.indentWithTabs  | Enable Tab Indentation |
| intro  | Flag For Displaying Introduction |
| creditScreen  | Flag To Enable Startup Logo |
| pluginsEnabled  | For Future Releases |

#
# Syntax Highlighting Support
| Sr No | Language |
| ------------- | ------------- |
| 1 | Python |
| 2 | HTML |
| 3 | JavaScript |
| 4 | CSS |
| 5 | Ruby |
| 6 | JSON |
| 7 | C++ |

# Logging System
Opulis has an extensive logging system. It is fully toggleable.

## Enabling/Disabling The Logging System

The Logging System can not be toggled in the config file. to enable it, create a file named `dev` in the same directory as the Opulis executable. Deleting the file automatically disables the logging system. A restart is required to toggle the logging system.

The Error Log however, can not be turned off. this is useful for debugging any crashes or unexpected behaviour.

### Logs are of 4 levels:

#### Info: Basic startup steps, Method calls etc
#### Debug: Config access, Logic etc
#### Warn: Log skips, ignorable errors
#### Error: Unexpected behaviour etc, can also be found in error file.

#
# Themes


## Ocean Theme ( Default )
![theme](/examples/ocean.png "THEMES")


## Dark Theme
![theme](/examples/dark.png "THEMES")


## Solarized Theme
![theme](/examples/solarized.png "THEMES")


## Blood Theme
![theme](/examples/blood.png "THEMES")


## Nature Theme
![theme](/examples/nature.png "THEMES")


## Cherry Theme
![theme](/examples/cherry.png "THEMES")


## Bloom Theme
![theme](/examples/bloom.png "THEMES")


## Radiant Theme
![theme](/examples/radiant.png "THEMES")


## Vanilla Theme
![theme](/examples/vanilla.png "THEMES")


# Syntax Themes

## Stheno Syntax Theme
![theme](/examples/stheno.png "S_THEMES")


## Medusa Syntax Theme
![theme](/examples/medusa.png "S_THEMES")


## Euryale Syntax Theme
![theme](/examples/euryale.png "S_THEMES")


# Status Bar
![theme](/examples/statusbar.png "STATUSBAR")


# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



