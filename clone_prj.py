import os
from sys import exit

projBasePath = ''

def makeLink(sourcePath, destinationPath):
    os.symlink(sourcePath, destinationPath)

def copyFile(sourcePath, destinationPath):
    with open(sourcePath, 'r') as source:
        with open(destinationPath,'w') as dest:
            for line in source:
                dest.write(line)


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
            os.system("git add {}".format(newFilePath))
            os.system("git add -f {}".format(os.path.join(newVPath, os.path.basename(link))))
        else :
            #newFilename = n[0] + "_" + destinationVe:rsion + n[1] 
            makeLink(realPath, os.path.join(newVPath, os.path.basename(link)))
            gitDoNotIgnore(os.path.join(newVPath, os.path.basename(link)))


def cloneVersion(projectPath, sourceVersion, destinationVersion):
    global projBasePath
    basePath = os.path.abspath(projectPath)
    projBasePath = basePath
    if (not (os.path.isdir(os.path.join(basePath, "dataset")) and os.path.isdir(os.path.join(basePath, "local")))):
        exit("Error - project directory not found")
    newVPath = os.path.join(basePath, "dataset", destinationVersion)
    currentVPath = os.path.join(basePath, "dataset", sourceVersion)
    if (not os.path.isdir(currentVPath)):
        exit("Could not find  current version path")

    print("Current v. path: " + currentVPath)
    print("New V path: " + newVPath)
    #crea cartella per nuova versione
    os.makedirs(newVPath, exist_ok = True)
    #elenca link simbolici nella cartella vecchia versione
    makeLinks(currentVPath, newVPath, destinationVersion, sourceVersion)
def main():
    print("Clone prj")

if __name__ == '__main__':
	main()
