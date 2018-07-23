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

FTP apps like Transmit and Cyberduck can synchronise content, but they are slow.

The CLI tool rsync is brilliant for this purpose in that it is lightning quick. The problem is that there is a lot to type in. There are a lot of flags to remember, as well as the username, IP address, the remote path, and the exclude file path. I also find it hard to remember to include a slash on the local and exclude a slash on the remote path. Meaning one can copy the entire repo into the wrong folder or just loose amongst your other stuff.

I used to do this kind of thing using Git and a Python library called fabric. Running the fabfile would commit, push, login to the remote server and then pull and restart. Whilst it was accurate it was a little clunky and again not super fast. I moved on from that to running a straight shell script. I ended up with variations of this script in each folder I made. 

This is where orite came in.

***

## Installation

    pip install orite

Or download the orite folder and alias orite.py in your bash profile.

    alias orite='python3 path-to-orite-folder/orite.py'


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

***

### Improvements
* Tests
* Enable the config file to have multiple servers. For example, if you use one server to run Django and another one to run Nginx. I don't want two sets of config and exclude files. I won't be able to do: `orite -^` which will upload to the default server and `orite -^ css` to the CSS one.
* Expand upon the diff feature
    * Potentially format the output so that it is easier to comprehend. 
    * From here one could manually copy across the bits they want or possibly do it programmatically. Choose from a numbered list? Which remote file/folder/s  would you like to copy to your local folder? i.e 1 or [2, 3] 
* Combine config and exclude files together.
* Investigate a safe mode? --backup flag and the scary delete after flag.
* The --info=flist flag only works in rysnc that is >= 3.1 Think about how to implement it so that older versions work too.
* Maybe there should be a rsync command flags option in the default config file. If it exists then the default command is overwritten.
* If it there is trouble connecting orite could look for an RSA key. If it exists then copy it to the server. If it doesn't then make one and copy it to the server.