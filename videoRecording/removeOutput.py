import os

def removefile():
    print("Remove Output File")
    if os.path.exists("output.txt"):
        if os.remove("output.txt"):
            print("File Removed")