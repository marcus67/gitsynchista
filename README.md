![gitsynchista icon](https://raw.githubusercontent.com/marcus67/gitsynchista/master/lib/gitsynchista_64.png)

# gitsynchista
Python tool for Pythonista to synchronize local files with a Github repository hosted on a WebDav server.

## Basic Functionality
The tool compares a local directory tree of Pythonista with a remote directory tree located on a WebDav server. It works very well (and sofar has only been tested with) the iOS app 'working copy'. The comparison is done by comparing the timestamps in both trees. New and updated files are transferred if required. So far there is no support for file deletion which should be done manually on both systems before synching. Synching of certain files can be suppressed using ignore files.

## Extented GUI Functionality
The tool can be called in GUI mode. The GUI offers additional functionality. Upon start it shows list of repositories configured for gitsynchista with their respective status.

<center><img src="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_without_working_copy.png" width="400"></center>

The user selects entries from the list to either show a modfification summary for each repository

<center><img src="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/modification_info.png" width="400"></center>

and trigger the synchronization. After synchronization the status will be updated automatically.

## Suport for "working copy"

The GUI mode has special support for the iOS app [working copy](https://itunes.apple.com/it/app/working-copy/id896694807?l=en). If at least one repository is configured to be synchronized with the WebDAV server of working copy gitsynchista will activate the WebDAV server automatically by using published url-schemes of working copy. The main window will contain addtional elements to reflect the support (see below).

<center><img src="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_with_working_copy.png" width="400"></center>

Also, the user will be able to open a selected repository in working copy directly from the gisynchista GUI by pressing a dedicated button (see screenhot above).

## Prerequirements

You need to have the Python WebDav client installed. See my clone at https://github.com/marcus67/easywebdav. Place the scripts into the `site-packages` directory. And, of course, you need to have a WebDav server. I'm using the iOS app [working copy](https://itunes.apple.com/it/app/working-copy/id896694807?l=en) but it should be possible to configure any other WebDAV server.

## Installation

The source code is available as a self-extracting Python script. See file `build/gitsynchista_zip.py`. Download this file and follow the instructions contained therein.

## Configuration

The tool gitsynchista does not require any configuration. However, the user will have to provide a small configuration file for each repository which needs to be synchronized. In its simplest form (which applies to a local synchronization with working copy) the configuration can be as simple as follows:

<pre>
[webdav]
epoch_delta = 3600

[repository]
name = SOME_LOGICAL_NAME
local_path = ../LOCAL_DIRECTORY_NAME
remote_path = /REMOTE_DIRECTORY_NAME
</pre>

It should be placed in some sub directory (preferably `etc`) of the application to be synchronized. For a detailed description of the configuration file see [the commented sample configuration file](https://raw.githubusercontent.com/marcus67/gitsynchista/master/etc/sample_gitsynchista_config).

## Feedback and Questions

For feedback (bug reports) [open an issue at GitHub](https://github.com/marcus67/gitsynchista/issues/new). If you have questions about the tool see the [Pythonista Forum](https://forum.omz-software.com/category/5/pythonista).

Have fun!
