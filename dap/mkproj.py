import os
from sys import exit


basePath =  os.getcwd()
projectName = ""
versionN = ""
functionalities = ['default']
useMake = False; useBMake = False; useSnakeMake = True


#Base folder tree to be created - all paths relative to PRJ_PATH
baseDirectories = [
        'dataset/',
        'local/bin', 'local/src/', 'local/env', 'local/rules',
        'local/config/', 'local/data/', 'local/modules',
    ]

#Files to be copied in the project. Destination is relative to PRJ_PATH; source files most be inside the model folder.
filesToCopy = {
    'default': [
        ['.gitignore', '.gitignore'],
        ['.envrc', '.envrc']
    ],
    'makeOrBmake': [
        ['makefile', 'local/rules/makefile'],
        ['_footer.mk', 'local/rules/_footer.mk'],
        ['_header.mk', 'local/rules/_header.mk']
    ],
    'make': [],
    'snakemake': [
        ['Snakefile','local/rules/Snakefile']
    ],
    'bmake': []
}
 
#Files to be created, paths relative to PRJ_PATH
filesToCreate = {
    'default': [],
    'make': [],
    'snakemake': [],
    'bmake': ['local/rules/bmakefile.mk'],
    'makeOrBmake': []
}
#Files to be created, paths relative to PRJ_PATH, where '_{versionName}' is added.
#i.e. local/src/example.txt a local/src/example_V1.txt
filesToCreateVersionSpecific = {
    'default': [],
    'make': [
        ['local/config/config', '.mk'], ['local/config/makefile_versioned', '.mk']
    ],
    'snakemake': [
        ['local/config/config', '.yaml'],
        ['local/config/Snakefile_versioned','.sk']
    ],
    'bmake': [
        ['local/config/config_bmake', '.mk'], ['local/config/bmakefile_versioned', '.mk']
    ],
    'makeOrBmake': []
}
#Sym links. Source path relative to PRJ_ROOT - destination relative to dataset/{projectVersion}
filesToLink = {
    'default': [], 
    'makeOrBmake': [
        ['local/rules/makefile', 'makefile']
    ],
    'bmake': [ ['local/rules/bmakefile', 'bmakefile'] ],
    'make': [],
    'snakemake': [['local/rules/Snakefile', 'Snakefile']]
}

#Sym links for version specific files. Source path relative to PRJ_ROOT - destination relative to dataset/{projectVersion}
#to source path '_{versionName}' is added.
#[['source', 'dest', 'sourceFormat']],
filesToLinkVersionSpecific = {
    'default':[], 
    'make': [
        ['local/config/config', 'config.mk', '.mk'], ['local/config/makefile_versioned', 'makefile_versioned.mk', '.mk']
    ],
    'snakemake': [
        ['local/config/config', 'config.yaml' , '.yaml'], 
        ['local/config/Snakefile_versioned', 'Snakefile_versioned.sk', '.sk']
    ],
    'bmake': [
        ['local/config/config_bmake', 'config_bmake.mk', '.mk'], ['local/config/bmakefile_versioned', 'bmakefile_versioned.mk', '.mk']
    ],
    'makeOrBmake': []
}

def makeFolder(path):
    os.makedirs(os.path.join(basePath, path), exist_ok = True)

def makeFile(path):
    with open(os.path.join(basePath, path), 'w') as f:
        f.write(' ')

def getRelativePath(path, fromPath):
    fromPath = os.path.split(fromPath)[0]
    return os.path.relpath(path, start=fromPath)

def makeLink(sourcePath, destinationPath):
    sourcePath = os.path.join(basePath, sourcePath)
    destinationPath = os.path.join(basePath, destinationPath)
    os.symlink(getRelativePath(sourcePath, destinationPath), destinationPath)
    #Aggiunge a git nonostante gitignore
    executionDir = os.getcwd()
    os.chdir(basePath)
    os.system("git add -f {}".format(destinationPath))
    os.chdir(executionDir)


#Copies a file - not very efficient way to do so but does not need any external dependency.
def copyFile(sourcePath, destinationPath):
    #Note: sourcePath is absolute path
    with open(sourcePath, 'r') as source:
        with open(os.path.join(basePath, destinationPath),'w') as dest:
            for line in source:
                dest.write(line)


def execute():
    #Updates paths for symlinks, adding dataset/{versionName}
    for functionality in functionalities:
        for link in filesToLink[functionality]:
            link[1] = os.path.join(basePath, "dataset",versionN, link[1])
    for functionality in functionalities:
        for link in filesToLinkVersionSpecific[functionality]:
            link[1] = os.path.join(basePath, "dataset",versionN, link[1])
        
    #Makes project directory
    if (os.path.isdir(basePath)):
        exit("Target project folder already exists.")
    os.makedirs(basePath, exist_ok=True)
    makeFolder("dataset/"+versionN)

    #Creates git repo
    executionDir = os.getcwd()
    os.chdir(basePath)
    os.system("git init")
    os.chdir(executionDir)

    #Creates the directory tree
    for directory in baseDirectories:
        makeFolder(directory)
    #Copies the files
    for functionality in functionalities:
        for fileToCopy in filesToCopy[functionality]:
            copyFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "model" ,fileToCopy[0]), fileToCopy[1])
    #Creates the new files
    for functionality in functionalities:
        for fileToCreate in filesToCreate[functionality]:
            makeFile(fileToCreate)
    for functionality in functionalities:
        for fileToCreateV in filesToCreateVersionSpecific[functionality]:
            makeFile(fileToCreateV[0] + "_" + versionN + fileToCreateV[1])
    #Makes symlinks
    for functionality in functionalities:
        for fileToLink in filesToLink[functionality]:
            makeLink(fileToLink[0], fileToLink[1])
    for functionality in functionalities:
        for fileToLink in filesToLinkVersionSpecific[functionality]:
            makeLink(fileToLink[0] + "_" + versionN + fileToLink[2], fileToLink[1])
     
    #Creates conda env; git commit.
    executionDir = os.getcwd()
    os.chdir(basePath)
    os.system("CONDA_BASE=$(conda info --base)")
    os.system("source $CONDA_BASE/etc/profile.d/conda.sh")
    os.system("conda create -n $(basename $PWD)_Env")
    os.system("conda activate $(basename $PWD)_Env")
    os.system("conda env export > local/env/environment.yml")
    os.system("git add .")
    os.system("git commit -m \"project created\"")
    os.chdir(executionDir)


def createProject(projectName_, projectVersion_, useSnakeMake_, useMake_, useBMake_):
    global basePath
    global projectName
    global versionN
    global functionalities
    global useMake; global useBMake; global useSnakeMake

    useBMake = useBMake_; useSnakeMake = useSnakeMake_; useMake = useMake_
    if (useBMake):
        functionalities.append('bmake')
    if (useSnakeMake):
        functionalities.append('snakemake')
    if (useMake):
        functionalities.append('make')
    if (useMake or useBMake):
        functionalities.append('makeOrBmake')
    projectName = projectName_
    versionN = projectVersion_
    basePath = os.path.join(os.getcwd(), projectName)
    execute()



def main():
    print('Mkproj')
    

if __name__ == '__main__':
	main()
