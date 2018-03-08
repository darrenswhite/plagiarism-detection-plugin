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

- Added basic boostrap form for posting new submissions. The form post is
currently a no-op.
- Added initial submission implementation in the Python server. The following
tutorial was used: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/.
- Submissions are now saved in the database but do not currently use
transactions. This should be addressed in the future but for now it should be
fine.
- Submissions are displayed on the student dashboard for the currently logged
in user.
- The sprint goal was reached but not all stories were completed. I caught the
flu and could not work much during the last half of the sprint. The remaining
stories will be moved into the next sprint. This sprint velocity is dramatically
low due to this.

## 26/02 - 04/03

- The previous sprint stories have been moved into this sprint and I will
continue to work on these for the rest of this sprint. I had to cancel my weekly
meeting on 26th due to the flu.
- Began initial work on the Python server unit tests (nose). The LDAP3
authentication was mocked to "bypass" logging in as a user. The next problem to
tackle is the mock or fake the MongoDB.
- Caught an ear infection this week and work has slowed to a halt. The flu has
passed so progress has resumed. This only allows for 2 days in this sprint and
may have to move the stories to next sprint again.
- Started using mockupdb today. Took a few hours to get used to using but I
managed to make a signin test for a user that has not signed in before. I had
to refactor some of the server code to allow for mocking the MongoDB (or so
I thought). Initially I thought I had to have a separate Server instance for
production and test environments (instance in \__init\__ for production) and
create another in each test setUp function. But the existing code relied
on importing and accessing the production instance so the tests would fail. I
solved this by making the tests mock the existing server instance - which is
the new mockdb method in server. The test will send a POST to the server to
signin (in a new thread) and mockupdb is then used to mock the database. Each
requested is retrieved and replied to while making assertions. The following
webpage proved very useful:
https://emptysqua.re/blog/test-mongodb-failures-mockupdb/.
- After creating the first signin test, it was very easy to add more. After
adding a second test it was time to refactor.

## 05/03 - 11/03

- This week I will work primarily on adding more tests, creating design
documents, and preparing for the mid-project demonstration.
