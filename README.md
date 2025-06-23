# ✨ Opulis Text Editor

**Opulis** is a minimal, open-source text editor built for the Windows Terminal. Lightweight, keyboard-driven, and highly customizable — it brings a TUI (Text-based User Interface) experience with modern flair.

---

## 📜 Features

- ⚡ Fast, minimal TUI interface — zero mouse required  
- 🧠 Smart hotkeys and theme control  
- 💾 Autosave with per-size tuning  
- 🎨 Built-in theme and syntax styling  
- 🪵 Verbose, toggleable logging system  
- 🔌 Future plugin support

---

## 🧱 The TUI System

Opulis runs entirely in the terminal, reducing system overhead and improving responsiveness. With full keyboard control, it’s ideal for power users, developers, or anyone who prefers clean, minimal workflows.

---

## 🚀 Quick Install

Paste this in PowerShell to install instantly:

```powershell
iwr -useb https://raw.githubusercontent.com/TheCamelCaseGuy/Opulis-Text-Editor/main/installer/installer.bat -OutFile "$env:TEMP\opulis_installer.bat"; & "$env:TEMP\opulis_installer.bat"
 | iex
```

✔️ Installs `Opulis.exe`, sets up the system PATH, and creates both Desktop and Start Menu shortcuts.

> 💡 After install, restart your terminal to activate the `opulis` command.

---

### 🗑️ To Uninstall

```powershell
iwr -useb https://raw.githubusercontent.com/TheCamelCaseGuy/Opulis-Text-Editor/main/installer/uninstaller.bat -OutFile "$env:TEMP\opulis_uninstaller.bat"; & "$env:TEMP\opulis_uninstaller.bat"

```

Cleans up everything: binaries, shortcuts, and the PATH entry.

---

## 🎹 Hotkeys

| Hotkey     | Action                 |
|------------|------------------------|
| Ctrl+S     | Save File              |
| Ctrl+O     | Open File              |
| Ctrl+Z     | Undo                   |
| Ctrl+N     | New Draft              |
| Ctrl+D     | Delete Line            |
| Ctrl+T     | Change Theme           |
| Ctrl+R     | Change Syntax Theme    |
| Ctrl+W     | Toggle Word Wrap       |
| Ctrl+L     | Open Settings File     |
| Tab        | Indent Line            |

> *More hotkeys and plugin bindings coming soon!*

---

## ⚙️ Configuration Options

Customize Opulis via a JSON-based config file:

| Path                          | Description                                   |
|-------------------------------|-----------------------------------------------|
| `appearance.theme`            | Editor color theme                            |
| `appearance.marginChar`       | Divider between line numbers and text         |
| `appearance.wordwrap`         | Toggle word wrap                              |
| `appearance.syntaxTheme`      | Syntax highlighting style                     |
| `autosave.enabled`            | Enable or disable autosave                    |
| `autosave.intervalSmall`      | Autosave interval (small files)               |
| `autosave.intervalLarge`      | Autosave interval (large files)               |
| `autosave.path`               | Folder where autosave files are stored        |
| `autosave.largeConsideration`| Char count threshold to qualify as "large"    |
| `hotkeys.tabSize`            | Number of spaces (or tabs) per indent         |
| `hotkeys.indentWithTabs`      | Use tab character vs spaces                   |
| `intro`                       | Show intro screen (true/false)                |
| `creditScreen`                | Show startup logo                             |
| `pluginsEnabled`              | Enable plugin support (experimental)          |

---

## 🎨 Themes

Opulis ships with 10 built-in themes:

| Theme       | Preview                             |
|-------------|--------------------------------------|
| Ocean       | ![Ocean](/examples/ocean.png)        |
| Dark        | ![Dark](/examples/dark.png)          |
| Solarized   | ![Solarized](/examples/solarized.png)|
| Blood       | ![Blood](/examples/blood.png)        |
| Nature      | ![Nature](/examples/nature.png)      |
| Cherry      | ![Cherry](/examples/cherry.png)      |
| Bloom       | ![Bloom](/examples/bloom.png)        |
| Radiant     | ![Radiant](/examples/radiant.png)    |
| Vanilla     | ![Vanilla](/examples/vanilla.png)    |

---

## 🧠 Syntax Highlighting Support

Opulis includes built-in syntax themes:

| Theme      | Preview                           |
|------------|------------------------------------|
| Stheno     | ![Stheno](/examples/stheno.png)    |
| Medusa     | ![Medusa](/examples/medusa.png)    |
| Euryale    | ![Euryale](/examples/euryale.png)  |

And supports highlighting for:

- Python
- JavaScript
- HTML/CSS
- JSON
- Ruby
- C++

---

## 🪵 Logging System

The logging system has four levels:

- **Info**: Startup steps, core methods  
- **Debug**: File I/O, config access  
- **Warn**: Soft errors or skipped logic  
- **Error**: Crashes and unhandled exceptions  

🛠 To enable logging, create a blank file named `dev` in the same folder as `Opulis.exe`.  
🧱 The error log is always on — for your safety.

---

## 💡 Status Bar
![Status Bar](/examples/statusbar.png)

Displays cursor position, mode, file name, and more.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---
