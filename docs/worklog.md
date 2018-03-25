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
- I have added a complete mid-project demonstration documentation file
containing notes on what will be presented.
- I have produced a basic architecture diagram should each of the components.
I have also created a detailed sequence diagram showing how a student interacts
with each component and how the components interact with each other.
- Did some minor refactoring, grouping all of the modules together and adding
appropriate iml and idea files to Git. Documentation files were moved from
the root into the docs directory.
- Added basic tests for the User class to ensure the class works as intended.
- Completed the goal for this milestone and created the milestone for the next
sprint.

## 12/03 - 18/03

- Added initial Python files for the post processor module. The base files
were taken from the server module. The Dockerfile used was also taken from the
server. To add a watch mechanism for the post processor proved more difficult
than expected. First, the database needed to be upgraded to MongoDB 3.6. This,
was the easy part. Next, the database was required to be a replica set for
watch to work. Looking through lots of guides, there was lots of manual work,
let alone only a few Docker tutorials. At first I thought I would have to add
redundancy to the database (i.e. 3 nodes instead of 1). This proved difficult
with the networking configuration. After the network issues were solved, more
problems were faced with not being able to vote for a master node. I then
decided to remove the 2 other nodes but the same problem was occurring. It
turned out to be that the master/primary node had to be initialized to setup
the replica set (only one time). It worked after initialization. But that was
manual initialization of the primary node. To automate this I wrote a bash
script which would check if its not initialized, and then initialize it. The
final issue was that, deploying the application a 2nd time would cause the
replica state to fail. It turns out the hostname would change each time, so the
fix was to change the hostname in the docker-compose.yml file.
- Trying to find how to identify code generation within the editor for the
plugin. The ActionManager provides a listener which could be used to identify
the menu action that was performed. It would be difficult to then identify the
following editor changes that were executed from that action. Another option
is to get the previous/last action performed when detecting editor changes. This
has a similar problem, when does the action end?
- Still haven't found a reasonable solution for detecting automatic code
generation. I have to ask myself, how much time should I spend trying to find
a solution? Can I continue without discrete identifications of source code?
On the other hand, while trying to find a solution for automatic code
generation, I did found a potential solution for detecting refactoring. I think
if I can detect renaming files and code then that would be enough for the
plugin. My primary focus should then shift toward the post-processor. This
week I have also been working on preparing for the mid-project demonstration. I
opted to use Google Slides to create a small presentation to aid with the demo.

## 19/03 - 25/03

- I have been researching machine learning techniques used to identify
plagiarism in source code. I have read many articles and have added them to
my references bibliography. I have added the latex files for the project report
to the `docs` directory. The front cover is complete and references have been
added (some still need annotations added). I aim to complete to abstract by
the end of this sprint.
- In terms of the post-processed data structure I will gather an XML file to
use as a working template (I will write a small project for this). I will
then generate template graphs that will be used on the staff dashboard. From
these graphs I will find what data will need to be stored in the database in
order to display these graphs.
- I've only thought about students being able to generate a fake XML file but
it has only now occurred to me that the XML could be modified before submission.
For example, replace source=CLIPBOARD with source=OTHER. The obvious way to
prevent this is encryption. Previously I had thought it was unnecessary. I
attempted to implement encryption (or to at least obfuscate the XML data). I
tried many methods. First, I tried obfuscating the file paths (the map keys).
This was successful and one way to expand on this would be to manually
obfuscate each value in the map. I played around with the code for a bit and
delved into the SDK source code. I found the XmlSerializer file. This file
handles serialising objects into an XML structure. Utilising this class I was
able to serialise the map into an XML string, then perform 128-bit AES
encryption on the XML string, then apply base64 encoding. The base64 is so that
it can be stored as a string. This string can then be saved as usual and will be
used for the persistent state. Upon loading the state, the process is simply
reversed. This prevents students from modifying the XML data.
- Due to implementing encryption at the end of this sprint, I was unable to
create the post-processed data structure. Instead I have moved this to next
sprint. To help create the data structure I will gather sample XML files from
other students writing a basic Java application. They will have the option
to "cheat" or plagiarise. I will ask them if they did so that I can identify
this in the recorded data. Aside from other students testing the plugin, I will
also write simple Java applications (the same one but in different ways) to
get a range of XML files.

## 26/03 - 01/04
