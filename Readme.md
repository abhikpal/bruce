# Readme

Bruce is a Python 3 script that helps you batch rename files using custom renaming masks.
See `bruce --help` for details.

> *Fourth Bruce*: Michael Baldwin, Bruce. Michael Baldwin, Bruce. Michael Baldwin, Bruce.
> *First Bruce*: Is your name not Bruce?
> *Michael*: No, it's Michael.
> *Second Bruce*: That's going to cause a little confusion.
> *Third Bruce*: Mind if we call you 'Bruce' to keep it clear? 
> 
> --- The Bruce Sketch. *Monty Python's Flying Circus*

## Requirements
Bruce was written in Python 3 on a machine running Debian 8.5. Bruce doesn't depend
on external libraries.

## Setup
Bruce doesn't need any fancy installers. Download the script, make it executable,
and create a soft link to the file.

```bash
$ # Clone the repo to a convenient location.
$ git clone http://www.github.com/abhikpal/bruce ~/utils/bruce/
$ 
$ # Make the file executable
$ chmod +x ~/utils/bruce/bruce.py
$
$ # create a soft link
$ # (make sure the folder is included in the system path!)
$ ln -s /home/`whoami`/utils/bruce/bruce.py /home/`whoami`/.bin/bruce
$
$ # You are done! Bruce is ready to rename your files.
$ # Just check the help page to double check your setup.
$ bruce --help
```

## Basic Usage

1. Use `bruce --generate` to generate a list of all the files in the current directory.
2. Edit the new csv file and add add required information
3. Follow up with `bruce --mask "mask" --data-source info_file.csv` to rename all the files. The `"mask"` is a string that will be used to rename the files. You can use the column headers from your csv file as placeholders by prefixing them with the `@` symbol. 

## Example workflow
```bash
$ ls
python01.txt  python02.txt  python03.txt  python04.txt  python05.txt
python06.txt
$
$ # To do a mass batch rename, we first generate an empty 
$ # csv file.
$ bruce --generate
$
$ # This gives us a new csv file we can edit.
$ ls
filelist_2016-09-06_2223.csv  python01.txt  python02.txt  python03.txt
python04.txt  python05.txt  python06.txt
$
$ # The output csv file contains a list of the files in the current directory
$ cat filelist_2016-09-06_2223.csv
filename
python01.txt
python02.txt
python03.txt
python04.txt
python05.txt
python06.txt
$
$ # We edit the csv file as required.
$ nano filelist_2016-09-06_2223.csv
$ cat filelist_2016-09-06_2223.csv
filename,fname,lname
python01.txt,Graham,Chapman
python02.txt,John,Cleese
python03.txt,Eric,Idle
python04.txt,Terry,Jones
python05.txt,Michael,Palin
python06.txt,Terry,Gilliam
$
$ # ...and now we call bruce again to finish the rename
$ bruce --mask "PYTHON - @lname, @fname.txt" --data-source filelist_2016-09-06_2223.csv
$ ls
changelog.csv  filelist_2016-09-06_2223.csv  PYTHON - Cleese, John.txt
PYTHON - Idle, Eric.txt    PYTHON - Palin, Michael.txt
PYTHON - Chapman, Graham.txt  PYTHON - Gilliam, Terry.txt
PYTHON - Jones, Terry.txt
$
$ # We don't need the csv file anymore
$ rm filelist_2016-09-06_2223.csv
$
$ # The changes will be logged in changelog.csv
$ cat changelog.csv
filename,oldname
PYTHON - Cleese%44 John.txt,python01.txt
PYTHON - Idle%44 Eric.txt,python02.txt
PYTHON - Palin%44 Michael.txt,python03.txt
PYTHON - Chapman%44 Graham.txt,python04.txt
PYTHON - Gilliam%44 Terry.txt,python05.txt
PYTHON - Jones%44 Terry.txt,python06.txt
$
$ # The changes can be reverted by doing:
$ bruce --revert
$ ls
changelog.csv  python01.txt  python02.txt  python03.txt  python04.txt  python05.txt
python06.txt
```
