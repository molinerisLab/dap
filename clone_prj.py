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
        if (os.path.isDir(os.path.join(current, "dataset"))):
            basePath = current 
            newVPath = os.path.join(basePath, "dataset", destinationVersion)
            if (os.path.isDir(os.path.join(basePath, "dataset", sourceVersion))):
                currentVPath = os.path.join(basePath, "dataset", sourceVersion)
                return
            else :
                 exit('Error - version ${sourceVersion} does not exist')
        basePath = os.path.dirname(basePath)
    exit('Error - you are not in a project directory')

def cloneVersion(sourceVersion, destinationVersion):
    findPaths(sourceVersion, destinationVersion)
    #crea cartella per nuova versione
    os.makedirs(newVPath, exist_ok = True)
    #elenca link simbolici nella cartella vecchia versione
    links = []
    for link in os.listdir(currentVPath):
        if (os.path.islink(link)):
            links.append(link)
    #crea copia di ogni file in local/
    for link in links:
        realPath =  os.listdir(link)
        fileName = os.path.basename(realPath)
        if (fileName.endwith("_"+sourceVersion)):
            newFilename = fileName.removesuffix(sourceVersion) + destinationVersion
        else :
            newFilename = fileName + "_" + destinationVersion
        newFilePath = os.path.join(os.path.dirname(realPath), newFilename)
        copyFile(realPath, newFilePath)
        makeLink(newFilePath, os.path.join(newVPath, os.path.basename(link)))


def main():
    print("Clone prj")

if __name__ == '__main__':
	main()
