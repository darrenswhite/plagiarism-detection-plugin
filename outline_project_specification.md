# Outline Project Specification

- IntelliJ plugin
  - Source code detection:
    - Detect keyboard events
    - Detect copy/paste
    - Detect code generation
    - Detect autocomplete popup
    - Detect refactoring
    - Detect external file changes
  - Investigate data structure for storing state (tree?)
  - Encrypt saved state to prevent modification
  - Settings user interface (user id or e-mail)

- Server
  - Investigate one-time or continuous upload
    - Could do both - implement one-time initially
  - Investigate implementation language (Go? Python?)
  - Investigate database storage (NoSQL?)
  - Docker support for encapsulated deployment
  - Front-end visual reports for lecturers (Bootstrap? PHP?)
