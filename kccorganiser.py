# This is a script to sort downloadeded comic/manga main/side chapters into volumes (semi-manually) and archive into .zip format/rename to .cbz extension for use in Kindle Comic Converter.
# There are some limitations with detecting some chapter formats; not able to sort chapters if they are in the wrong format, ie. Chapter 29, Chapter 30...
# A function to clean up the chapter names is provided and sort out names like`~`, 'Chapter 3 Vol2' or 'Z= 3', however, it won't recognise chapters if they have numbers before the chapter number, ie. 'S2 - Chapter 4'.
# You would require a separate script to remove those extra details pertaining to your case of folders.

import shutil, time
from pathlib import Path
from sys import platform

def exiter():
    try:
        input("\nQuitting, have a nice day.\n\nPress <ENTER> to exit. (Or <Ctrl> + C if you're feeling spicy.)\n")
    except KeyboardInterrupt:
        exit()

def cleanUp(): # cleans up chapter names into usable format
    timeStart = time.time()
    for file in root.iterdir(): # all files in directory
        if file.is_dir(): # all folders in directory
            folderName = file.name
            spaces = 0
            numbers = list()
            
            for char in folderName:
                if char == " ":
                    spaces += 1 # space counter
                elif spaces > 1: # catches chapters with names like 'Chapter 101 Vol2...'
                    break
                    folderName = " ".join(folderName.split(" ")[:2])
                elif char.isdigit(): # takes chapter number from numbers in folder name
                    numbers.append(char) # does not work if there are numbers before chapter number ie. S2..
                     
            while numbers[0] == "0":
                numbers.pop(0) # removes 0's before actual chapter number
                
            
        if file.is_dir():
            newFolderName = "Chapter " + "".join(numbers)
            source = str(root / folderName)
            destination = str(root / newFolderName)
            try:
                shutil.move(source, destination)
            except OSError:
                print("\nFolder not found. Probably wrong format.")
                    
    print("\nChapter names cleaned up in " + str(round(time.time() - timeStart, 2)) + " seconds!")
                
    
def mainChapterSorting(): # sorts chapters into volumes
    try:
        numberOfVolumes = int(input("\nNumber of volumes to sort into? "))
    except ValueError:
        print("\nPlease enter a valid integer number of volumes.")
        exiter()
    volumeStart = input("\nStarting volume number? (Default = 1): ")
    chapterStart = input("\nStarting chapter number? (Default = 1): ")
    
    timeStart = time.time()
    
    if (chapterStart == "") or (chapterStart == "1"):
        chapterCurrent = 1 # default chapter to start from
    else:
        chapterCurrent = int(chapterStart)
    
    if (volumeStart == "") or (volumeStart == "1"):
        volumeCurrent = 1 # default volume to start from
    else:
        volumeCurrent = int(volumeStart)
    
    for volume in range(numberOfVolumes): # iterates through all volumes
        print("\nCreating \'Volume " + str(volumeCurrent + volume) + "\' ...")
        try:
            chapterEnd = int(input("From chapter " + str(chapterCurrent) + " to... ")) # last chapter in volume
        except ValueError:
            print("\nPlease enter a valid integer end chapter for \'" + str(volumeCurrent + volume) + "\'.")
            exiter()
        for chapter in range(chapterEnd - chapterCurrent + 1):
            source = root / ("Chapter " + str(chapterCurrent + chapter))
            destination = root / ("Volume " + str(volumeCurrent + volume)) / ("Chapter " + str(chapterCurrent + chapter))
            try:
                shutil.move(source, destination)
            except OSError: 
                print("\nFolder not found. Chapter number was probably wrong.")
                exiter()
        chapterCurrent = chapterEnd + 1
    print("\nFinished creating " + str(numberOfVolumes) + " volume(s) in " + str(round(time.time() - timeStart, 2)) + " seconds!")

def sideChapterSorting(): # sorts side chapters into volumes
    timeStart = time.time()
    source = list()
    destination = list()
    if platform == "win32": # FIX FOR WINDOWS VS UNIX PATHS SEPARATOR
        sep = "\\\\"
    else:
        sep = "/"
    for file in root.iterdir(): # finds all files in root directory
        if (file.suffix != "") and (file.is_dir()): # filters by inclusion of decimal point and being a folder
            childName = file.name # only the name of the side chapter is pulled and is the source path
            source.append(file)
        
            parentName = childName.split(".")[0] # takes the first part of side chapter as the main chapter to find
            for parent in root.glob("*/" + parentName):
                volume = str(parent).split(sep)[-2]# volume to put side chapter in ///// tested for mac for now..
                path = root / volume / childName # destination path
                destination.append(path)

    for chapter in range(len(source)):
        shutil.move(source[chapter], destination[chapter])
    print("\nFinished sorting " + str(len(source)) + " side chapter(s) into their volume(s) in " + str(round(time.time() - timeStart, 2)) + " seconds!")

def conversion():
    timeStart = time.time()
    name = root.name
    oldFile = name + ".zip"
    newFile = name + ".cbz"
    base =  root.parents[0] # directory above root directory to place .zip file
    print("\nCreating archive...")
    shutil.make_archive(root, "zip", base, name) # places .zip archive in the directory above the manga/comic directory
    Path.rename((base / oldFile), (base / newFile))
    print("\n\'" + oldFile + "\' was created and renamed to \'" + newFile + "\' in " + str(round(time.time() - timeStart, 2)) + " seconds!")
    print("\'" + newFile + "\' is located at \'" + str(base) + "\' .")
    toDelete = input("\nDo you want to remove the source directory \'" + str(root) + "\'? (Y/N) (Default = Y): ")
    timeStart = time.time()
    if (toDelete == "") or (toDelete == "y") or (toDelete == "yes") or (toDelete == "Y") or (toDelete == "Yes") or (toDelete == "YES"):
        shutil.rmtree(root) # recursively delete source folder
        print("\nDeleted \'" + str(root) + "\' in " + str(round(time.time() - timeStart, 2)) + " seconds!")
    elif (toDelete == "n") or (toDelete == "no") or (toDelete == "N") or (toDelete == "No") or (toDelete == "NO"):
        print("\n\'" + str(root) + "\' has NOT been deleted.")
    else:
        print("\nNo more changes have been made as no option was selected.")

try:
    root = Path(input("\nDirectory of the comic/manga? (Example: /Users/aaronshiu/Documents/HakuNeko/Tower of God: ")) # cross-platform file paths
    print("\nComic/manga directory: \'" + str(root) + "\'.")
except:
    print("\nThat path does not exist.")
    exiter()

print("\nIf chapter names are not of format, ie. \'Chapter 29\', please use option \'1\' first. *Cannot accept chapters where there are other numbers before chapter number, ie. \'S2 - Chapter 29\'")    
firstOption = input("\nChoose a number from the following options. Default = 1: \n\n1) Clean up chapter names into usable format.\n2) Sort main chapters into volumes.\n3) Sort side chapters into volumes. (Requires (2) to have been completed first.)\n4) Archive the directory into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC). ")

if (firstOption == "") or (firstOption == "1") or (firstOption == "one") or (firstOption == "One") or (firstOption == "ONE"): # clean up chapter names
    print() # runs through all options
    cleanUp()
    option = input("\nDo you want to sort main chapters into volumes? (Y/N) Default = Y: ")
    if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
        mainChapterSorting()
    elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
        print("\nNothing has been changed.")
    option = input("\nAre there any side chapters to sort? (Y/N) Default = N: ")
    if (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
        sideChapterSorting()
        option = input("\nDo you want to archive the source directory \'" + str(root) + "\' into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC)? (Y/N) Default = Y: " )
        if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
            conversion()
        elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
            option = input("\nDo you want to archive the source directory \'" + str(root) + "\' into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC)? (Y/N) Default = Y: " )
            if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
                conversion()
            elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
                print("\nNothing has been changed.")
    else:
        option = input("\nDo you want to archive the source directory \'" + str(root) + "\' into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC)? (Y/N) Default = Y: " )
        if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
            conversion()
        elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
            option = input("\nDo you want to archive the source directory \'" + str(root) + "\' into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC)? (Y/N) Default = Y: " )
            if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
                conversion()
            elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
                print("\nNothing has been changed.")

elif (firstOption == "2") or (firstOption == "two") or (firstOption == "Two") or (firstOption == "TWO"): # main chapter sorting
    print() # runs through sorting options and archiving/renaming
    mainChapterSorting()
    option = input("\nAre there any side chapters to sort? (Y/N) (Default = N): ")
    if (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
        sideChapterSorting()
        option = input("\nDo you want to archive the source directory \'" + str(root) + "\' into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC)? (Y/N) Default = Y: " )
        if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
            conversion()
        elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
            option = input("\nDo you want to archive the source directory \'" + str(root) + "\' into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC)? (Y/N) Default = Y: " )
            if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
                conversion()
            elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
                print("\nNothing has been changed.")
            else:
                print("\nNo changes have been made as no option was selected.")
        else:
            print("No changes have been made as no option was selected.")
    elif (option == "") or (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
        print("\nNothing has been changed.")
    else:
        print("\nNo changes have been made as no option was selected.")
        
elif (firstOption == "3") or (firstOption == "three") or (firstOption == "Three") or (firstOption == "THREE"): # side chapter sorting
    print() # runs through side chapter sorting and archiving
    sideChapterSorting()
    option = input("\nDo you want to archive the source directory \'" + str(root) + "\' into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC)? (Y/N) Default = Y: " )
    if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
        conversion()
    elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
        option = input("\nDo you want to archive the source directory \'" + str(root) + "\' into a .zip file and rename the extension to .cbz for Kindle Comic Converter (KCC)? (Y/N) Default = Y: " )
        if (option == "") or (option == "y") or (option == "yes") or (option == "Y") or (option == "Yes") or (option == "YES"):
            conversion()
        elif (option == "n") or (option == "no") or (option == "N") or (option == "No") or (option == "NO"):
            print("\nNothing has been changed.")
        else:
            print("\nNo changes have been made as no option was selected.")
    else:
        print("\nNo changes have been made as no option was selected.")
            
elif (firstOption == "4") or (firstOption == "four") or (firstOption == "Four") or (firstOption == "FOUR"): # archiving and renaming
    print() # runs through just archiving/renaming
    conversion()
    
else:
    print("\nNo opton was selected.")
exiter()

# To-do:
# Taking volume/chapter lists from online sites to automate entire process
# Only use archiving/renaming option when all chapters are sorted into volumes; maybe delete remaining extra chapters that aren't in volumes?
