import os
from sys import exit
from git import Repo, Submodule

projBasePath = ''


#Se eccezione a livello di bash -> rimettere tutto a posto
#Far andare link direttamente a local

#Clones the repo, if not already existing; verifies the existence of dataset/{moduleVersion} and retururns path
def clone(R_Url, path, moduleVersion):
    repoName = R_Url.split("/")[-1]
    if (repoName.endswith('.git')):
        repoName = repoName.removesuffix('.git')
    rPath = os.path.join(path ,repoName)
    #Repo could exist already
    if (os.path.isdir(rPath)):
        if (os.path.isdir(os.path.join(rPath, "dataset", moduleVersion))):
            return rPath
        else:
            exit("Repository does not contain version {}".format(moduleVersion))
    #If not, it clones it
    os.makedirs(rPath, exist_ok = True)
    repo = Repo(projBasePath)
    Submodule.add(repo, repoName, rPath, R_Url)
    if (os.path.isdir(os.path.join(rPath, "dataset", moduleVersion))):
        return rPath
    #If repo does not contain dataset/versionName, undo the cloning and return error
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git rm {}".format(rPath))
    os.system("git commit -m \"Failed to add module {}\"".format(repoName))
    os.chdir(executionDir)
    exit("Could not clone repository, or repository is not compliant")



def getRelativePath(path, fromPath):
    fromPath = os.path.split(fromPath)[0]
    return os.path.relpath(path, start=fromPath)

def makeLink(sourcePath, destinationPath):
    os.symlink(getRelativePath(sourcePath, destinationPath), destinationPath)
    #Adds to gitignore
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git add -f {}".format(destinationPath))
    os.chdir(executionDir)

def makeLinks(newModulePath, versionPath):
    for file in os.listdir(newModulePath):
        file_ = os.path.join(newModulePath, file)
        if (os.path.isdir(file_)):
            #If it is folder, it creates new folder and recursively links the contents 
            os.makedirs(os.path.join(versionPath, file), exist_ok=True)
            makeLinks(file_, os.path.join(versionPath, file))
        else :
            makeLink(file_,  os.path.join(versionPath, os.path.basename(file)))
            #Aggiunge a git nonostante gitignore
            executionDir = os.getcwd()
            os.chdir(projBasePath)
            os.system("git add -f {}".format(os.path.join(versionPath, os.path.basename(file))))
            os.chdir(executionDir)

def add_module(R_Url, versionPath, moduleVersion):
    global projBasePath
    projBasePath = os.getenv('PRJ_ROOT')
    if (projBasePath == None or not os.path.isdir(projBasePath)):
        exit("Could not find base project directory")
        
    versionPath = os.path.join(projBasePath, versionPath)
    if (not os.path.isdir(projBasePath)):
        exit("Project root does not exist")
    if (not os.path.isdir(versionPath)):
        exit("Version path does not exist")

    newModule = clone(R_Url, os.path.join(projBasePath, "local", "modules"), moduleVersion)

    newModulePath = os.path.join(newModule, "dataset", moduleVersion)
    os.makedirs(os.path.join(versionPath, os.path.basename(newModule)), exist_ok = True)
    versionPath = os.path.join(versionPath, os.path.basename(newModule))
    os.makedirs(versionPath, exist_ok = True)
    makeLinks(newModulePath, versionPath)

    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git commit -m \"Module {} added\"".format(R_Url))
    os.chdir(executionDir)
