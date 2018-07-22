# orite 
### An opinionated rsync wrapper written in Python

The purpose of orite is to synchronise folders and files between a remote and local server.

FTP apps like Transmit and Cyberduck can synchronise content, but they are slow.

The CLI tool rsync is brilliant for this purpose in that it is lightning quick. The problem is that there is a lot to type in. There are a lot of flags to remember, as well as the username, IP address, the remote path, and the exclude file path. I also find it hard to remember to include a slash on the local and exclude a slash on the remote path. Meaning one can copy the entire repo into the wrong folder or just loose amongst your other stuff.

I used to do this thing using Git and a Python library called fabric. Running the fabfile would commit, push, login to the remote server and then pull and restart. Whilst it was accurate it was a little clunky and again not super fast. I moved on from that to running a straight shell script. I ended up with variations of this script in each folder I made. 

__*This project is an effort to centralise a sync approach, add options, future functionality, and do it using Python.*__


### ōrite is a Māori word for ʻthe same’
It's pronounced [like this](https://s3.amazonaws.com/media.tewhanake.maori.nz/dictionary/4802.mp3) rather than ‘oh-right’.

***

## Installation

    pip install orite

Or download the orite folder and alias orite.py in your bash profile.

    alias orite='python3 path-to-orite-folder/orite.py'


## How to run?
Running the following for the first time, preferably above the folder you are looking to sync, will make a config file and a default exclude file.

    orite

Then

    orite -^ 

Will upload

    orite -v

Will download. By default, orite will run in dry-run mode. Use the `-r` flag to override this.

***

### Improvements
* How does this directory differ from the remote one?
    Whilst we can run rsync with the dry run flag the feedback you get is unsatisfactory. rsync will tell you that files differ, but if you want to know exactly what the difference is, which lines, for example, you are out of luck.

    diff is great with this kind of thing, but getting diff to run over a network is slow.

    1. So the suggested solution is to make an invisible copy of the local folder to `_orite_copy__<folder_name>`
    2. Sync from the remote folder to the copy
    3. run `diff -r -N  <folder_name> _orite_copy__<folder_name>/ --exclude-from <path-to>/_orite_exclude.txt`

    Potentially format the output so that it has a better hierarchy and is clearer.
    From here one could manually copy across the bits they want or possibly do it programmatically. Like:

    $ These are the file/folder/s that differ
    \1. filename 
    \2. filename
    \3. whole_folder_name 
    \4. __all__
    Which remote file/folder/s  would you like to copy to your local folder? i.e 1 or [2, 3]

* Enable the config file to have multiple servers. For example, I use one server to run Django and a different one for Nginx. I don't want two sets of config and exclude files. I won't be able to do: `orite -^` which will upload to the default server and `orite -^ css` to the CSS one.
* Investigate a safe mode? --backup flag and the scary delete after flag.
* The --info=flist flag only works in rysnc that is >= 3.1 Think about how to implement it so that older versions work too.
* Maybe there should be a rsync command flags option in the default config file. If it exists then the default command is overwritten.
* If it there is trouble connecting orite could look for an RSA key. If it exists then copy it to the server. If it doesn't then make one and copy it to the server.