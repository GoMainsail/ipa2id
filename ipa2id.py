try:
    import plistlib, zipfile, os
    from tkinter.filedialog import askopenfilename
    from tkinter import Tk
except:
    print("This tool requires tkinter, plistlib, os and zipfile modules to function correctly!")
def new_ipa():

    Tk().withdraw() # Hides tkinter window

    fil = askopenfilename(title="Select an IPA archive", filetypes = (("iPhone Application Archive","*.ipa"),("Compressed folder", "*.zip"),("all files","*.*")))
    # shows file open

    try:
        zpf = zipfile.ZipFile(fil)
        # zip object
    except:
        print("An error occurred in importing the file as a ZIP Archive!")
        os.system('pause')
        exit()

    try:
        namespace = [item for item in zpf.namelist() if item.lower().endswith(".app/info.plist")][0]
        # gets path of info.plist
    except:
        print("An error occurred when trying to find the IPA information!")
        os.system('pause')
        exit()

    info = zpf.open(namespace) # opens binary plist

    info_r = info.read() # reads plist data

    try:
        final_id = plistlib.loads(info_r) # loads binary as dictionary
    except:
        print("An error occurred when trying to decode the bundle information!")
        os.system('pause')
        exit()

    print("--------------------------------------------")
    try:
        print(final_id['CFBundleDisplayName']) # display name
    except:
        try:
            print(final_id['CFBundleExecutable'])
        except:
            print(fil)
    print(final_id['CFBundleIdentifier']) # bundle id

    yn = input("Find another Bundle ID? (Y/N) ")
    if yn.lower()=="y":
        new_ipa()
    else:
        exit()

new_ipa()