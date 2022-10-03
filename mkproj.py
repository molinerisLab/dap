import os
from sys import exit

#Variabili da inizializzare con argomenti
basePath =  os.getcwd()
projectName = ""
versionN = ""
functionalities = ['default']
useMake = False; useBMake = False; useSnakeMake = True


#Scheletro delle cartelle del progetto - relative a basePath
baseDirectories = [
        'dataset/',
        'local/bin', 'local/src/', 'local/env', 'local/rules',
        'local/config/', 'local/data/', 'local/modules',
    ]

#Files da copiare nel progetto. destination relativa a basePath; file di origine devono essere nella cartella model
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
    'snakemake': [],
    'bmake': []
}
 
#Files da creare, path relativi a basePath
filesToCreate = {
    'default': [],
    'make': [],
    'snakemake': ['local/rules/Snakefile.mk'],
    'bmake': ['local/rules/bmakefile'],
    'makeOrBmake': []
}
#Files da creare, path relativi a basePath - al cui nome viee aggiunto _versionN
#es da local/src/esempio.txt a local/src/esempio_V1.txt
filesToCreateVersionSpecific = {
    'default': [],
    'make': [
        ['local/config/config', '.mk']
    ],
    'snakemake': [
        ['local/config/config', '.yaml']
    ],
    'bmake': [
        ['local/config/config_bmake', '.mk']
    ],
    'makeOrBmake': []
}
#Link. Path source relativo a basePath - dest relativo a dataset/{projectVersion}
filesToLink = {
    'default': [], #[ ['source', 'dest']],
    'makeOrBmake': [
        ['local/rules/makefile', 'makefile']
    ],
    'bmake': [ ['local/rules/bmakefile', 'bmakefile'] ],
    'make': [],
    'snakemake': [['local/rules/Snakefile.mk', 'cluster.yaml']]
}

#Link. Path source relativo a basePath ma con aggiunta di _versionN
#es local/rules/makefile -> local/rules/makefile_V1
filesToLinkVersionSpecific = {
    'default':[], #[['source', 'dest', 'sourceFormat']],
    'make': [
        ['local/config/config', 'config.mk', '.mk']
    ],
    'snakemake': [
        ['local/config/config', 'config' , '.yaml']
    ],
    'bmake': [
        ['local/config/config_bmake', 'config_bmake.mk', '.mk']
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

#Copiare il file leggendo riga per riga non è molto efficiente
#però evita di dover importare librerie esterne e rende un po' più snello il progetto
def copyFile(sourcePath, destinationPath):
    #Nota: sourcePath deve essere path assoluto - non relativo a basePath
    with open(sourcePath, 'r') as source:
        with open(os.path.join(basePath, destinationPath),'w') as dest:
            for line in source:
                dest.write(line)


def execute():
    #Aggiorna path per i link aggiungendo dataset/{versione}
    for functionality in functionalities:
        for link in filesToLink[functionality]:
            link[1] = os.path.join(basePath, "dataset",versionN, link[1])
    for functionality in functionalities:
        for link in filesToLinkVersionSpecific[functionality]:
            link[1] = os.path.join(basePath, "dataset",versionN, link[1])
        
    #Crea cartella per progetto
    if (os.path.isdir(basePath)):
        exit("Target project folder already exists.")
    os.makedirs(basePath, exist_ok=True)
    makeFolder("dataset/"+versionN)

    #Crea repo git
    executionDir = os.getcwd()
    os.chdir(basePath)
    os.system("git init")
    os.chdir(executionDir)

    #Crea le directory
    for directory in baseDirectories:
        makeFolder(directory)
    #Copia i file di default nelle directory create 
    for functionality in functionalities:
        for fileToCopy in filesToCopy[functionality]:
            copyFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), "model" ,fileToCopy[0]), fileToCopy[1])
    #Crea i file da creare nuovi
    for functionality in functionalities:
        for fileToCreate in filesToCreate[functionality]:
            makeFile(fileToCreate)
    for functionality in functionalities:
        for fileToCreateV in filesToCreateVersionSpecific[functionality]:
            makeFile(fileToCreateV[0] + "_" + versionN + fileToCreateV[1])
    #Crea link
    for functionality in functionalities:
        for fileToLink in filesToLink[functionality]:
            makeLink(fileToLink[0], fileToLink[1])
    for functionality in functionalities:
        for fileToLink in filesToLinkVersionSpecific[functionality]:
            makeLink(fileToLink[0] + "_" + versionN + fileToLink[2], fileToLink[1])
     
    #CONDA: crea environment; GIT: Aggiunge file ed esegue commit
    executionDir = os.getcwd()
    os.chdir(basePath)
    os.system("CONDA_BASE=$(conda info --base)")
    os.system("source $CONDA_BASE/etc/profile.d/conda.sh")
    os.system("conda create -n $(basename $PWD)Env")
    os.system("conda env export > local/env/environment.yml")
    os.system("git add .")
    os.system("git commit -m \"project created\"")
    os.chdir(executionDir)

#Per esecuzione di mkproj da dap.py
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
