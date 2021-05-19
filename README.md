# Pipeline

This pipeline is designed to manage data collected in a certain behavioral field study.
As such, its usecase is currently limited to a very narrow set of operations on specific files of known format.
It is also an ongoing project, with more functionality being implemented whenever the need arises and/or the developer's schedule allows for it.

## Table of contents
* [Structure](#structure)
* [Setup](#setup)
* [Basic operation](basic-operation)

## Structure

Within the `python` folder, there a multiple scripts that may be used individually, with some of the scripts depending on the previous execution of others.
For example, `make_schedule.py` expects to find files that were previously created - or updated - by `rectifier.py`; namely, a file within `misc_files` called `protocol_list.csv`.

Here is a table of scripts that may be called and a short explanation of what they are intended for:

Script name | Description
----------- | -----------
`make_schedule.py` | Create a "schedule", i.e. an overview of which individual has been observed at what times, and consequently could or should be observed again in the near future.
`errors.py` | Iterate through all rectified files in the dataset and check for common mistakes, then output `errors.csv` in the main folder, listing the errors with additional info on where they occured.

##Setup

To set the pipeline up for the first time, make sure to download (or git clone) this project to your machine. in case of downloading, extract the compressed file you received to a folder of your choosing (desktop might be most convenient).
make sure that `python 3+` is installed on the machine, and the `pandas` library is available (issue `pip install pandas` in your terminal/command prompt).
Lastly, create a folder titled `data` within the main folder of the project and dump all of your recorded files (and their parent folders) in.
When those criteria are all met, you are good to go and use the scripts included here for your project.

## Basic operation

### Windows (10)

Assuming a `pipeline` folder - mirroring the one provided here - is present on the Desktop, open a terminal by launching "cmd" from your start menu.
Then, navigate to the `python` subfolder by typing `cd Desktop\pipeline\python` in the terminal (and hitting [Enter]).
Note that the current directory in the terminal can be checked with the `dir` command. When the output of `dir` shows the python script names, you will have managed to find the correct directory. Congratulations.

Now, scripts can be called via the command `python <script_name>`, where `<script_name>` refers to, and should be replaced by, the actual script you want to execute.
On execution, scripts might output some information to the terminal.

Usually, it is best to ignore such output and wait for the terminal to show you the same prompt symbol that was seen when you first opened it.
Oftentimes, that would be ">".
This indicates that the script you called has terminated and further actions would be possible on your part.
When you executed all scripts that you wanted to, you may at this point simply close the terminal window.

In case the output shown in the terminal contains an error message and/or a traceback, consult an expert on how to avoid any damages or mitigate their impact ASAP.

Who you gonna call?

