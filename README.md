# gitsynchista
Python tool for Pythonista to synchronize local files with a Github repository hosted on a WebDav server.

## Basic Functionality
The tool compares a local directory tree of Pythonista with a remote directory tree located on a WebDav server. It works very well (and sofar has only been tested with) the iOS app 'working copy'. The comparison is done by comparing the timestamps in both trees. New and updated files are transferred if required. So far there is no support for file deletion which should be done manually on both systems before synching. Synching of certain files can be suppressed using ignore files.

## Installation

The easiest 