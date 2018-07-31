# orite 
## An opinionated rsync wrapper written in Python

The purpose of orite is to synchronise folders and files between a remote and local server.

To do this using orite run:

    orite -^ 

To do this using rsync run:

    rsync --human-readable --info=flist --stats --archive --verbose --partial -ic --progress --dry-run /Users/username/Documents/websites/site_name/stack/folder/ username@127.68.551.54:/root/stack/folder --exclude-from="exclude.txt"

This project is an effort to centralise a sync approach, configure once, add options, and make it simple.

#### ōrite is a Māori word for ʻthe same’
It's pronounced [like this](https://s3.amazonaws.com/media.tewhanake.maori.nz/dictionary/4802.mp3) rather than ‘oh-right’.

***

## The problem

FTP apps like Transmit and Cyberduck are good apps and can synchronise content, but they are slow.

The CLI tool rsync is brilliant for this purpose in that it is lightning quick. The problem is that there is a lot to type in. There are a lot of flags to remember, as well as the username, IP address, the remote path, and the exclude file path. I also find it hard to remember to include a slash on the local and exclude a slash on the remote path. Meaning one can copy the entire repo into the wrong folder or just loose amongst your other stuff.

I used to do this kind of thing using Git and a Python library called fabric. Running the fabfile would commit, push, login to the remote server and then pull and restart. Whilst it was accurate it was a little clunky and again not super fast. I moved on from that to running a straight shell script. I ended up with variations of this script in each folder I made. 

This is where orite came in.

***

## Installation

    pip3 install orite

Or download the orite folder and alias orite.py in your bash profile.

    alias orite='python3 path-to-orite-folder/orite.py'

## Update

	pip3 install orite --upgrade --no-cache-dir


## How to run?
Run orite in the directory above the folder that you would like to sync.

If you haven't used orite in this directory you will be prompted to lay down a config file and a exclude file.

To upload

    orite -^ 

To download

    orite -v

By default, orite will run in dry-run mode. Use the `-r` flag to override this and do a sync for real.

The help menu can be seen using

    orite -h


## Multiple servers – one config file

You can enable the config file to have more than one server or folder location. For example, my DEFAULT folder is my Django install and in a very separate location is my CSS folder. 

`orite -^` will upload (with --dry-run set) to my DEFAULT setting, and 
`orite CSS -^` will upload to my CSS section settings. 

Open the config file in your text editor. Add a section label at the bottom like so
`[CSS]`
Then add the `path_to_local_folder = /path/` on the next line and `path_to_remote_folder = /path/` to the next. If your CSS settings are on the same server then you don't need to add those details again. Needless to say that if they are on a different server than add those different settings to this section too.

Add as many sections as you like.

Run `orite -s` to get a print out of all the sections in your config file.


## Improvements

See issues for enhancements.