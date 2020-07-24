# Plagiarism Detection Plugin

This project is aimed to help identify plagiarism or UAP (Unacceptable Academic
Practice) for software related projects.

## Requirements

- Plugin
    - IntelliJ IDEA 2017.3 (build 173.0) or higher
- Server & post-processor
    - Docker (tested with 18.03.0-ce)
    - Docker compose (tested with 1.8.0)

## Installation

> Note: Ensure requirements have been installed

### Plugin

To install the plugin using the .JAR file follow the instructions
[here](https://www.jetbrains.com/help/idea/installing-plugin-from-disk.html).

While the plugin is installed, each project is tracked for plagiarism and the result is stored in .idea/plagiarism_detection.xml. This XML file can be uploaded to the server to be processed.

### Server and post-processor

To start both the server and post-processor use `./run.sh`. This will use
`docker-compose` to deploy both containers. To access the server, visit
`localhost:8000`.

The server uses the Aberystwyth LDAP server for authentication and must be
connected to the `eduroam` network.

To enable debugging, use `PDP_DEBUG=1 ./run.sh`.

## Worklog

View the worklog [here](docs/worklog.md).
