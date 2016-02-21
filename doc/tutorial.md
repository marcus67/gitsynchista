![gitsynchista icon](https://raw.githubusercontent.com/marcus67/gitsynchista/master/lib/gitsynchista_64.png)

# Step-by-Step Tutorial for gitsynchista

This is a step-by-step tutorial to use gitsynchista with Pythonista. It shows the usage of the GUI mode only since
the functionality of the command-line mode is rather limited.

## Prerequisites

  * You will need Pythonista. You probably are aware of this since would not have found your way to this page in the first place. Currently, only the 2.* version of Pythonista is supported but this will hopefully change soon.
  * You will need a WebDav server hosting your repository. This can be hosted on an iDevice-local repository such as the iOS app [working copy](https://itunes.apple.com/it/app/working-copy/id896694807?l=en) but it should be possible to configure any other WebDAV server.
  * You need to have the Python WebDav client installed. See my clone at https://github.com/marcus67/easywebdav. Place the script `easywebdav/client.py` into the `site-packages` directory. 
  * Install gitsynchista itself by downloading the [self-extracting archive](https://github.com/marcus67/gitsynchista/blob/master/build/gitsynchista_zip.py), placing it into the root directory of your Pythonista app and executing the script. Afterwards you will have a `gitsynchista` subdirectory. The downloaded can then be deleted.

## Preparing the First Repository on the WebDav Server

The main task of gitsynchista is to synchronize the files of a repository located on your iDevice with the corresponding 
repository on the WebDAV server (which may also be on the iDevice as mentioned above). If you already have such a repository 
you are all set to start. Otherwise create such a repository on your WebDav server. Of course, how this is done is outside
the scope of this tutorial.

From now on we assume that the repository has the path `/myproject` on the WebDav server. 

## Preparing the Same Repository with gitsynchista

The next step will be create a base directory in the Pythonista directory structure. Although it is not really required it is usually a good practive to use the same directory name in Pythonista. So from now on we assume that the base directory is called `myproject`.

