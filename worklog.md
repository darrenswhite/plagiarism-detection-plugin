# Work log

## 29/01 - 04/02

- Looked at the IntelliJ Platform Plugin SDK
- Created a Hello World plugin
  - Store String with PersistentStateComponent and AnAction
  - Used the GitHub plugin as a working example
  - Detect keystrokes, found two options:
    - TypedHandlerDelegate (doesn't work when auto complete popup is shown)
    - TypedHandler (auto complete popup doesn't work properly)
- Researched existing detection tools (MOSS, Turnitin)
  - These are used after work is submitted

## 05/02 - 11/02

- Started the OPS (Outline Project Specification)
- Prepared for OPS presentation
- Found another detection method:
  - Attach a DocumentListener to EditorFactory#EditorEventMulticaster
  - This allows tracking Document changes which could be:
    - Typed, copy-pasted, generated, external, etc.
  - For now, using this instead of TypedHandler/Delegate.
  - This will track all changes in each file without knowing where it came from
- Added copy-paste detection by comparing the DocumentEvent fragment
with the CopyPasteManager contents
  - This doesn't work well with external editors (i.e pasting in Vim) when the
  project is closed
