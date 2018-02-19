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
- Tracking changes are now stored in the workspace.xml file. A change has the
properties:
  - Path: the file path that was changed
  - Offset: where the change was made
  - Old String: the String that was removed/replaced
  - New String: the String that was inserted
  - Source: the type of change (e.g. typed, copy-paste, etc.)
  - Timestamp: when the change was made
- Made Settings persistent with the application not per project - previously
users had to enter their credentials per project
- Added external change detection. These changes aren't saved yet as an
algorithm will need to be written to check what has changed.
- External change detects when files are deleted
- .idea directory is ignored when tracking changes

## 12/02 - 18/02

- Added algorithm to detect external file changes
  - This uses the IntelliJ SDK for diffs (com.intellij.diff)
- Added copy-test test
- Contacted Alun Jones (auj@aber.ac.uk) about LDAP for Aber server auth
- Added external change detection test
- Created a small Python script to test the following:
  - LDAP auth with Aber
  - Parse XML recorded data
  - Store submissions with MongoDB
- This sprint was completed halfway through the week. I will need to
re-evaluate my velocity for the next sprint. For now I will add new stories
to this sprint
- Added Flask to the server for web pages. I'm using flask-login and ldap3
for user authentication. I used a bootstrap template for the login page
- Implemented bootstrap dashboard for staff and students
- Added Docker container for the Python server and MongoDB. Docker compose is
used to deploy each of the containers. A Bash script is used to run the docker
compose commands easily

## 19/02 - 25/02
