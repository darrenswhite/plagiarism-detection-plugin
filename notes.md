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

### Post-processing

- Process data to check for different authors (i.e different author copy-paste)
- Check timestamps to find anything odd (i.e coder is usually slow but changed
speed so might be copying)
- Possibly add some machine learning classification with supervised learning

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

# Flow

1. Plugin records data
2. Student clicks submit menu button
3. Browser opens and is directed to the server URL
4. User is prompted to authenticate with Shibboleth (Aber)
5. Plugin sends recorded data to server along with authentication data
