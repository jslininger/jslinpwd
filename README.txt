Password manager I made out of paranoia. Designed for use on Linux using either CLI or GTK3 as GUI. 

CLI commands: 
python(3) - some distros have different ways of calling python3, so this command depends on that.
python(3) jslinpwd.py -e site - prints new password after running and adds "site: password" to the list. If site exists, overrides old password with new one.
python(3) jslinpwd.py -d site1 site2 .. - decrypts the passwords listed (potentially infinite). Approximates passwords that are not found.
python(3) jslinpwd.py - displays full list of passwords
python(3) jslinpwd.py -r site - removes the site and password from list
TODO: add multiple sites to -r and -e options. Create additional character requirements as command line arguments

GUI usage:
python(3) ui.py - way to start from terminal. On my machine I statically compiled the program and created a .desktop file, but those are options I will add at a later time.
With the gui open, after you have inputted your password to access your .gpg file, the passwords will be listed alphanumerically by site (no password).
To get the password, select a site and press the copy button on the button, which will copy the password to your clipboard and pasted anywhere you need.
The window is scrollable if the amount of passwords exceeds the size of window. The window is also resizable.
TODO: add buttons to create/delete passwords. 

Dependencies:
Python3.10 is what is was developed and tested on. Likely works on older versions that support the following modules:
python: fuzzywuzzy, python-levenshtein; both of which can be installed via pip.
TODO: make dependencies optional, as they are only useful for string approximation, which every user might not use.

GPG: required to create my .gpg files to encrypt and decrypt. Comes with every Linux distro to my knowledge. 
.gpg file is currently required to create before running the program and is hard coded in its path.
TODO: create initialization and maybe integrate with gpg to easily create new .gpg files, save .gpg files in standard location for linux, such as .local/share

GTK: required to run the gui. 
TODO: Make dependency optional for those that do not have gtk installed.
