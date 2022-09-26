import os
from sys import exit
basePath = ""
currentVPath = ""
newVPath = ""

def makeLink(sourcePath, destinationPath):
    os.symlink(sourcePath, destinationPath)

def copyFile(sourcePath, destinationPath):
    with open(sourcePath, 'r') as source:
        with open(destinationPath,'w') as dest:
            for line in source:
                dest.write(line)

def findPaths(sourceVersion, destinationVersion):
    global basePath; global currentVPath; global newVPath
    current = os.getcwd()
    for i in range(3):
        if (os.path.isdir(os.path.join(current, "dataset"))):
            basePath = current 
            newVPath = os.path.join(basePath, "dataset", destinationVersion)
            if (os.path.isdir(os.path.join(basePath, "dataset", sourceVersion))):
                currentVPath = os.path.join(basePath, "dataset", sourceVersion)
                return
            else :
                 exit('Error - version ${sourceVersion} does not exist')
        basePath = os.path.dirname(basePath)
    exit('Error - you are not in a project directory')

def cloneVersion(sourceVersion, destinationVersion):
    findPaths(sourceVersion, destinationVersion)
    print("Current v. path: " + currentVPath)
    print("New V path: " + newVPath)
    #crea cartella per nuova versione
    os.makedirs(newVPath, exist_ok = True)
    #elenca link simbolici nella cartella vecchia versione
    links = []
    for link in os.listdir(currentVPath):
        link_ = os.path.join(currentVPath, link)
        print("File: "); print(link)
        if (os.path.islink(link_)):
            print("Islink");
            links.append(link_)
        else:
            print("Not a link, sorry")
    #crea copia di ogni file in local/
    for link in links:
        realPath =  os.path.realpath(link)
        fileName = os.path.basename(realPath)
        n = os.path.splitext(fileName)
        if (n[0].endswith("_"+sourceVersion)):
            newFilename = n[0].removesuffix(sourceVersion) + destinationVersion + n[1]
            newFilePath = os.path.join(os.path.dirname(realPath), newFilename)
            copyFile(realPath, newFilePath)
            makeLink(newFilePath, os.path.join(newVPath, os.path.basename(link)))
        else :
            #newFilename = n[0] + "_" + destinationVersion + n[1] 
            makeLink(realPath, os.path.join(newVPath, os.path.basename(link)))

def main():
    print("Clone prj")

if __name__ == '__main__':
	main()
