import os
from sys import exit

projBasePath = ''

def getRelativePath(path, fromPath):
    fromPath = os.path.split(fromPath)[0]
    return os.path.relpath(path, start=fromPath)

def makeLink(sourcePath, destinationPath):
    os.symlink(getRelativePath(sourcePath, destinationPath), destinationPath)
    #Aggiunge a git nonostante gitignore
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git add -f {}".format(destinationPath))
    os.chdir(executionDir)

def copyFile(sourcePath, destinationPath):
    with open(sourcePath, 'r') as source:
        with open(destinationPath,'w') as dest:
            for line in source:
                dest.write(line)
    #Aggiunge a git nonostante gitignore
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git add {}".format(destinationPath))
    os.chdir(executionDir)


def makeLinks(currentVPath, newVPath, destinationVersion, sourceVersion):
    links = []
    for link in os.listdir(currentVPath):
        link_ = os.path.join(currentVPath, link)
        if (os.path.islink(link_)):
            links.append(link_)
        elif (os.path.isdir(link_)):
            os.makedirs(os.path.join(newVPath, link) , exist_ok = True)
            makeLinks(link_, os.path.join(newVPath, link), destinationVersion, sourceVersion)
        
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
            makeLink(realPath, os.path.join(newVPath, os.path.basename(link)))


def cloneVersion(sourceVersion, destinationVersion):
    global projBasePath
    projBasePath = os.getenv('PRJ_ROOT')
    if (projBasePath == None or not os.path.isdir(projBasePath)):
        exit("Could not find base project directory")
        

    if (not (os.path.isdir(os.path.join(projBasePath, "dataset")) and os.path.isdir(os.path.join(projBasePath, "local")))):
        exit("Error - project directory not found")
    newVPath = os.path.join(projBasePath, "dataset", destinationVersion)
    currentVPath = os.path.join(projBasePath, "dataset", sourceVersion)
    if (not os.path.isdir(currentVPath)):
        exit("Could not find  current version path")

    #crea cartella per nuova versione
    os.makedirs(newVPath, exist_ok = True)
    #elenca link simbolici nella cartella vecchia versione
    makeLinks(currentVPath, newVPath, destinationVersion, sourceVersion)
    #Esegue commit git
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git commit -m \"Version {} created\"".format(destinationVersion))
    os.chdir(executionDir)

def main():
    print("Clone prj")

if __name__ == '__main__':
	main()