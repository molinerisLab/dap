import os
import argparse
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
filesToCopy = [
    ['.gitignore', '.gitignore'],
    ['.envrc', '.envrc']
]
#Files da creare, path relativi a basePath
filesToCreate = {
    'default': [],
    'make': ['local/rules/makefile'],
    'snakemake': ['local/rules/Snakefile.mk'],
    'bmake': ['local/rules/rules.mk']
}
#Files da creare, path relativi a basePath - al cui nome viee aggiunto _versionN
#es da local/src/esempio.txt a local/src/esempio_V1.txt
filesToCreateVersionSpecific = {
    'default': [],
    'make': [
        ['local/config/makefile', '']
    ],
    'snakemake': [
        ['local/config/config', '.yaml']
    ],
    'bmake': [
        ['local/config/config', '.sk']
    ]
}
#Link. Path source relativo a basePath - dest relativo a dataset/{projectVersion}
filesToLink = {
    'default': [], #[ ['source', 'dest']],
    'make': [['local/rules/makefile', 'makefile']],
    'snakemake': [['local/rules/Snakefile.mk', 'cluster.yaml']],
    'bmake': [['local/rules/rules.mk','config.sk']]
}

#Link. Path source relativo a basePath ma con aggiunta di _versionN
#es local/rules/makefile -> local/rules/makefile_V1
filesToLinkVersionSpecific = {
    'default':[], #[['source', 'dest', 'sourceFormat']],
    'make': [
        ['local/config/makefile', 'config', '']
    ],
    'snakemake': [
        ['local/config/config', 'config' , '.yaml']
    ],
    'bmake': [
        ['local/config/config', 'config', '.sk']
    ]
}

def makeFolder(path):
    os.makedirs(os.path.join(basePath, path), exist_ok = True)

def makeFile(path):
    with open(os.path.join(basePath, path), 'w') as f:
        f.write(' ')

def makeLink(sourcePath, destinationPath):
    os.symlink(os.path.join(basePath, sourcePath), os.path.join(basePath, destinationPath))

#Copiare il file leggendo riga per riga non è molto efficiente
#però evita di dover importare librerie esterne e rende un po' più snello il progetto
def copyFile(sourcePath, destinationPath):
    #Nota: sourcePath deve essere path assoluto - non relativo a basePath
    with open(sourcePath, 'r') as source:
        with open(os.path.join(basePath, destinationPath),'w') as dest:
            for line in source:
                dest.write(line)

def removeBasePathPrefix(path):
    return os.path.relpath(path, start=basePath)

def execute():
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

    #Crea le directory
    for directory in baseDirectories:
        makeFolder(directory)
    #Copia i file di default nelle directory create 
    for fileToCopy in filesToCopy:
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
     
    #Crea repo git
    executionDir = os.getcwd()
    os.chdir(basePath)
    os.system("git init")
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

    useBMake = useMake_; useSnakeMake = useSnakeMake_; useMake = useBMake_
    if (useBMake):
        functionalities.append('bmake')
    if (useSnakeMake):
        functionalities.append('snakemake')
    if (useMake):
        functionalities.append('make')
    projectName = projectName_
    versionN = projectVersion_
    basePath = os.path.join(os.getcwd(), projectName)
    execute()



#Per esecuzione di mkproj come standalone
def parseArguments():
    global basePath
    global projectName
    global versionN
    global functionalities
    global useMake; global useBMake; global useSnakeMake;

    parser = argparse.ArgumentParser(description='Create the local/ directory structure for a prj and a skeleton based on prjname and version')
    parser.add_argument('projectname', metavar='PROJ_NAME', type=str, nargs=1,
                    help='Name of the project to create')
    parser.add_argument('projectversion', metavar='PROJ_VERSION', type=str, nargs=1,
                    help='Version of the project - es. V1')

    parser.add_argument('--make', dest='make', const=True, default=False, nargs='?',
                    help='Generate makefile files')
    parser.add_argument('--bmake', dest='bmake', const=True, default=False, nargs='?',
                    help='Generate bmakefile files')
    parser.add_argument('--snakemake', dest='snakemake', const=True, default=True, nargs='?',
                    help='Generate Snakemake files')


    args = parser.parse_args()
    useBMake = args.bmake; useSnakeMake = args.snakemake; useMake = args.make
    if (useBMake):
        functionalities.append('bmake')
    if (useSnakeMake):
        functionalities.append('snakemake')
    if (useMake):
        functionalities.append('make')
    projectName = args.projectname[0]
    versionN = args.projectversion[0]
    basePath = os.path.join(os.getcwd(), projectName)

def main():
    #Inizializza variabili da argomenti
    parseArguments()
    execute()
    

if __name__ == '__main__':
	main()
