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

From now on we assume that the repository has the path `/dummyproject` on the WebDav server. 

## Preparing the Same Repository with gitsynchista

The next step will be create a base directory in the Pythonista directory structure. Although it is not really required it is usually a good practive to use the same directory name in Pythonista. So from now on we assume that the base directory is called `dummyproject`.

Now, create a configuration file named `gitsynchista_config.txt` in the base directory or the `etc` subdirectory with the following content:

    [repository]
    local_path = ../dummyproject
    remote_path = /dummyproject


This is the minimal configuration. Note that the path for `remote_path` is absolute on the WebDav server whereas the path for `local_path` is relative to the location of the script `gitsynchista.py`. You may need to add credentials to log into the WebDav server by using the para meters `username` and `password`:


    [repository]
    local_path = ../dummyproject
    remote_path = /dummyproject
    username = myloginin
    password = mypassword


If you intend to use working copy as your WebDav server you must also add a value to correct for different handling of the timestamps and see to it that working copy is "woken up" by gitsynchista. So, in this case your configuration file would look like this:

	[webdav]
	epoch_delta = 3600
	[repository]
	local_path = ../dummyproject
	remote_path = /dummyproject
	working_copy_wakeup = True

## Creating an Action Shortcut

The easiest way to call gitsynchista is to create an Pythonista Action Shortcut. Press the wrench symbol in the Pythonista top bar (you have to be in a script to see the wrench).

![action shortcut step 1](https://raw.githubusercontent.com/marcus67/gitsynchista/master/action_shortcut_step1.png)

Press the "Edit" button to add a new shortcut.

![action shortcut step 2](https://raw.githubusercontent.com/marcus67/gitsynchista/master/action_shortcut_step2.png)

Choose an empty slot by pressing the plus sign.

![action shortcut step 3](https://raw.githubusercontent.com/marcus67/gitsynchista/master/action_shortcut_step3.png)

Choose the `gitsynchista` script and optionally add a logical name, an icon and the icon color. Save the settings.

## Calling the GUI
Start the GUI by using the Action Menu Entry or by starting the script `gitsynchista.py` without any parameters. If everything is configured correctly the GUI will start up showing this:

![sync step 1](https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step1.png)


![sync step 2](https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step2.png)


![sync step 2 info](https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step2_info.png)


![sync step 3](https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step3.png)


![sync done](https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_done.png)

## Error Handling

![sync step 1](https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step1_error.png)

![sync step 1](https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step1_error_info.png)

