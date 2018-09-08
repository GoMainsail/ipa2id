try:
    import plistlib, zipfile, os, ntpath
    from tkinter.filedialog import askopenfilename, askdirectory
    from tkinter import Tk
except:
    print("This tool requires tkinter, ntpath, plistlib, os and zipfile modules to function correctly!")
def new_ipa():

    Tk().withdraw() # Hides tkinter window
    fil = []
    ask = input("Please input 'i'/'ipa' for single ipa or 'a'/'all' for all in folder: ")
    if ask.lower() == "i" or ask.lower()=="ipa":
        fil.append(askopenfilename(title="Select an IPA archive", filetypes = (("iPhone Application Archive","*.ipa"),("Compressed folder", "*.zip"),("all files","*.*"))))
    elif ask.lower() == "a" or ask.lower()=="all":
        batch = askdirectory(title="Select a folder")
        for fname in [os.path.join(batch, f) for f in os.listdir(batch) if os.path.isfile(os.path.join(batch, f)) and f.endswith(".ipa")]:
            fil.append(fname)
    else:
        print("Invalid option!")
        exit()
    # shows file open

    for item in fil:
        try:
            zpf = zipfile.ZipFile(item)
            # zip object
        except:
            print("An error occurred in importing the file as a ZIP Archive!")
            continue

        try:
            namespace = [item for item in zpf.namelist() if item.lower().endswith(".app/info.plist")][0]
            # gets path of info.plist
        except:
            print("An error occurred when trying to find the IPA information!")
            continue

        info = zpf.open(namespace) # opens binary plist

        info_r = info.read() # reads plist data

        try:
            final_id = plistlib.loads(info_r) # loads binary as dictionary
        except:
            print("An error occurred when trying to decode the bundle information!")
            continue

        print("--------------------------------------------")
        try:
            print("{} ({})".format(final_id['CFBundleDisplayName'],ntpath.basename(item))) # display name
        except:
            try:
                print("{} ({})".format(final_id['CFBundleExecutable'], ntpath.basename(item)))
            except Exception as e:
                print("Unknown error")
                print(e)
                print(item)
        print(final_id['CFBundleIdentifier']) # bundle id

    print("--------------------------------------------")
    yn = input("Find another Bundle ID? (Y/N) ")
    if yn.lower()=="y":
        new_ipa()
    else:
        exit()

new_ipa()