import os
from sys import exit
from git import Repo



def clone(R_Url, path):
    rPath = os.path.join(path ,R_Url.split("/")[-1])
    os.makedirs(rPath, exist_ok = True)
    repo = Repo.clone_from(R_Url, rPath)
    if (repo):
        if (os.path.isdir(repo.working_tree_dir)):
            return repo.working_tree_dir
        exit("Could not clone git repo")

#Temp - versione di clone che non richiede librerie esterne
"""def clone(R_Url, path):
    executionDir = os.getcwd()
    os.chdir(path)
    files = os.listdir(path)
    os.system("git clone " + R_Url)
    os.chdir(executionDir)
    newFiles = os.listdir(path)
    created = list(set(newFiles).difference(set(files)))
    if (created.length == 0):
        exit("Repository could not be cloned")
    for file in created:
        if os.path.isdir(file):
            return file 
    exit("Error cloning repository")"""

def add_module(projectRoot, R_Url, versionPath, moduleVersion):
    #verifica esistenza di projectRoot e di versionPath
    versionPath = os.path.join(projectRoot, versionPath)
    print(versionPath)
    if (not os.path.isdir(projectRoot)):
        exit("Project root does not exist")
    if (not os.path.isdir(versionPath)):
        exit("Version path does not exist")
    #clona repo
    newModule = clone(R_Url, os.path.join(projectRoot, "local", "modules"))
    print(newModule)
    #recupera path con link da copiare
    newModulePath = os.path.join(newModule, "dataset", moduleVersion)
    print("New module target directory: " + newModulePath)
    if (not os.path.exists(newModulePath)):
        os.system("rm -rf " + newModule)
        exit("Module does not contain dataset/"+moduleVersion)
    os.makedirs(os.path.join(versionPath, os.path.basename(newModule)), exist_ok = True)
    versionPath = os.path.join(versionPath, os.path.basename(newModule))
    os.makedirs(versionPath, exist_ok = True)
    for file in os.listdir(newModulePath):
        file_ = os.path.join(newModulePath, file)
        os.symlink(file_, os.path.join(versionPath, os.path.basename(file)))
