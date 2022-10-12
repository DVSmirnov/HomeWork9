-----------------------------------Main information---------------------------------

The script analyzes logs, saves results to json file and displays results in console. 
The information displayed in the console is duplicated into a json file

-----------------------------The algorithm of the program---------------------------

1. Launching the program with indication of a folder or file as a key, or not
2. Estimation of file size, duration of its processing
3. Analysis of the log file, data processing, output of analytical information to the console, 
followed by recording this information in a file in the format .json. The name of the resulting 
json file is unique because of the date and time in the header. The resulting json file is 
created in the same directory where the executable file is located main.pyIf the log file is fully 
processed by the script, the program terminates.
