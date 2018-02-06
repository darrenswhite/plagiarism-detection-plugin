# General overview

- IntelliJ IDEA plugin
- Record keystrokes
- Send keystrokes to server
- Store user uid (for authentication/identification)
- Server to generate reports for users

# Implementation ideas

## Tree data structure

- Tree structure (similar to files and directories)
- Record keystrokes for each file

## Identifying unacceptable academic practice

- Compare keystrokes to total character count
- Flag files with low KCR (keystroke-character-ratio)
- Flag source code which is copy/pasted
- Flag source code which was externally modified
- Detect the origin of source code:
    - Manually typed
    - Copy/paste
    - Code generation
    - Auto complete
    - Refactoring
    - Externally modified
- Possibly use IntelliJ IDEA local history
- Use timestamps when source code is added

## Server

### One-time upload

- Upload a file containing keystroke data once completed

#### Advantages

- Easy offline support
  - Only requires internet connection to upload file

#### Disadvantages

- File may be modified by user before uploading

### Continuous upload

- Continuously send keystroke data to server

#### Advantages

- Key stroke information less vulnerable to modification

#### Disadvantages

- Requires internet connection (unless offline is supported)

# FAQ

- Will hard copies be required for submission?
  - No
