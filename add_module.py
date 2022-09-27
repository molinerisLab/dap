import os
from sys import exit
from git import Repo, Submodule

projBasePath = ''

def clone(R_Url, path):
    repoName = R_Url.split("/")[-1]
    rPath = os.path.join(path ,repoName)
    os.makedirs(rPath, exist_ok = True)
    repo = Repo(projBasePath)
    Submodule.add(repo, repoName, rPath, R_Url)
    if (os.path.isdir(os.path.join(rPath, "dataset"))):
        return rPath
    #Se no errore
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git rm --cached {}".format(rPath))
    os.chdir(executionDir)
    exit("Could not clone repository, or repository is not compliant")



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

def makeLinks(newModulePath, versionPath):
    for file in os.listdir(newModulePath):
        file_ = os.path.join(newModulePath, file)
        if (os.path.isdir(file_)):
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
    #clona repo
    newModule = clone(R_Url, os.path.join(projBasePath, "local", "modules"))
    #recupera path con link da copiare
    newModulePath = os.path.join(newModule, "dataset", moduleVersion)
    if (not os.path.exists(newModulePath)):
        os.system("rm -rf " + newModule)
        exit("Module does not contain dataset/"+moduleVersion)
    os.makedirs(os.path.join(versionPath, os.path.basename(newModule)), exist_ok = True)
    versionPath = os.path.join(versionPath, os.path.basename(newModule))
    os.makedirs(versionPath, exist_ok = True)
    makeLinks(newModulePath, versionPath)

    #Esegue commit git
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git commit -m \"Module {} added\"".format(R_Url))
    os.chdir(executionDir)
