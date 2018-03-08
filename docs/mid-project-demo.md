# Mid-Project Demonstration

## Introduction

- IntelliJ IDEA, IDE by JetBrains
- Plugin developed using the IntelliJ Platform Plugin SDK
- Track how a student writes codes (for assignments)
- Identify plagiarism or UAP (Unacceptable Academic Practice)
- Other detection tools only analyse the final piece of work
    - MOSS (Measure Of Software Similarity) developed by Stanford

### Major components

> _Show component diagram_
- Plugin
- Server (and database)
- Post-processor

## Plugin

### Current progress

> _Show XML file_
- Detects file changes
    - Keyboard
    - Copy/paste
    - External file changes
- Map: File path for keys, List of changes for values
- Saved in an XML file
- JUnit 4

### Future development

- Detect more methods
    - Automatic code generation
    - Autocomplete
    - Refactoring
- Encrypt XML
    - Doesn't look possible with the SDK

### Misc

- Generating fake XML file
    - A lot of work
    - If you can do it, you can do the assignment
- Ethics
    - Tracking user keyboard within the IDE editor

## Server

### Current progress

- Python 3 Flask application
- Students and lecturers can login
    - Aberystwyth credentials via LDAP
- Students can view own submissions
- Staff can view all students' submissions
- Students can submit recorded data
- Submissions are stored in a persistent database
    - MongoDB
    - No complex queries were needed
    - XML easy to store as a BSON document
- Docker container support
    - Uses Docker compose
- Nose, unittest, mock, mockupdb

### Future development

- Allow resubmissions for students
- Add submission filtering for staff
- Add pagination to dashboard
- Use database transactions
- Add filter to show submissions identified as plagiarism / UAP

## Post-processor

### Current progress

- None
- Will _watch_ the database for new submissions
- Separate service from the server
- Python 3

### Future development

- Identify level of plagiarism / UAP for each submission
- Methods:
    - Considerable amounts of copy/paste
    - Considerable amounts of external file changes
    - Total time spent per project or file
    - Differences in behavioural coding patterns (speed and habits)
    - Machine learning classification using controlled training datasets
- How to gather training / testing data?
